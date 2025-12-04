import concurrent
import enum
import os
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

from PySide6.QtCore import Qt, Slot, QThreadPool
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QHeaderView, QMenu

from helpers.build_tree_runnable import BuildTreeRunnable
from utils import path_analysis, byte_size_to_str, create_tree_item
from constants import PathType


class FileTree(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.thread_pool = QThreadPool.globalInstance()
        self.itemChanged.connect(self.on_item_changed)

    def contextMenuEvent(self, e) -> None:
        item = self.itemAt(e.pos())
        if item is not None:
            context = QMenu(self)
            open_dir_action = QAction('打开文件夹', self)

            @Slot()
            def _open_file_dir():
                if item.data(0, Qt.ItemDataRole.UserRole) == PathType.FILE:
                    # 选中文件
                    subprocess.run(f'explorer /select,"{item.toolTip(0)}"', shell=True)
                else:
                    os.startfile(item.toolTip(0))

            open_dir_action.triggered.connect(_open_file_dir)
            context.addAction(open_dir_action)
            context.exec(e.globalPos())

    @Slot()
    def on_item_changed(self, item: QTreeWidgetItem, col):
        if col != 0:
            return
        self.blockSignals(True)
        # 勾选目录时，同步子节点
        if item.data(0, Qt.ItemDataRole.UserRole) == PathType.DIR:
            self._async_child_check_state(item, item.checkState(0))
        # 同步父节点
        if item.parent() is not None:
            self._all_check_parent(item.parent(), item.checkState(0))
        self.blockSignals(False)

    @Slot()
    def select_all(self):
        self.blockSignals(True)
        root = self.invisibleRootItem()
        self._check_all(root, Qt.CheckState.Checked)
        self.blockSignals(False)

    @Slot()
    def unselect_all(self):
        self.blockSignals(True)
        root = self.invisibleRootItem()
        self._check_all(root, Qt.CheckState.Unchecked)
        self.blockSignals(False)

    def _check_all(self, parent: QTreeWidgetItem, check_state: Qt.CheckState):
        for i in range(parent.childCount()):
            child = parent.child(i)
            child.setCheckState(0, check_state)
            if child.childCount() > 0:
                self._check_all(child, check_state)

    # 判断父节点下是否所有子节点都勾选了或未勾选，并设置父节点状态
    def _all_check_parent(self, parent: QTreeWidgetItem, check_state: Qt.CheckState):
        all_correct = True
        for i in range(parent.childCount()):
            child = parent.child(i)
            if child.checkState(0) != check_state:
                all_correct = False
                break
        if all_correct:
            parent.setCheckState(0, check_state)
        else:
            parent.setCheckState(0, Qt.CheckState.PartiallyChecked)
        if parent.parent() is not None:
            self._all_check_parent(parent.parent(), check_state)

    # 同步子节点状态
    def _async_child_check_state(self, parent: QTreeWidgetItem, check_state: Qt.CheckState):
        for i in range(parent.childCount()):
            child = parent.child(i)
            child.setCheckState(0, check_state)
            self._async_child_check_state(child, check_state)
            if child.childCount() > 0:
                self._async_child_check_state(child, check_state)

    def _get_checked_item(self, current_item: QTreeWidgetItem, checked_items):
        """
        递归获取所有勾选的节点
        :param current_item: 当前遍历到的节点
        :param checked_items: 所有勾选的节点，是个元组，(目录节点, 文件节点)
        :return: checked_items
        """
        dir_items, file_items = checked_items

        path_type = current_item.data(0, Qt.ItemDataRole.UserRole)
        if path_type is not None:
            if path_type == PathType.FILE and current_item.checkState(0) == Qt.CheckState.Checked:
                file_items.append(current_item)
            elif path_type == PathType.DIR and current_item.checkState(
                    0) == Qt.CheckState.Checked and current_item.childCount() == 0:
                dir_items.append(current_item)
        if current_item.childCount() > 0:
            for i in range(current_item.childCount()):
                checked_items = self._get_checked_item(current_item.child(i), checked_items)
        return checked_items

    # 获取所有已勾选项
    def all_checked_items(self):
        root = self.invisibleRootItem()
        return self._get_checked_item(root, ([], []))

    def all_check_parent(self, parent, check_state: Qt.CheckState):
        self._all_check_parent(parent, check_state)

    def _get_parent_item(self, node_map, parent_path):
        if parent_path not in node_map:
            pth = parent_path.split(os.sep)[-1]
            parent_item = create_tree_item(pth, parent_path, True, '', '')
            node_map[parent_path] = parent_item
            parent_parent_path = os.path.abspath(os.path.join(parent_path, '..'))
            parent_parent_item = self._get_parent_item(node_map, parent_parent_path)
            parent_parent_item.addChild(parent_item)
        return node_map[parent_path]

    def load_tree(self, search_tgt_dir, tree_node_queue):
        self.blockSignals(True)
        self.clear()

        node_map = {
            search_tgt_dir: self.invisibleRootItem()
        }

        data_queue = Queue()

        while not tree_node_queue.empty():
            rab = BuildTreeRunnable(data_queue, tree_node_queue.get())
            self.thread_pool.start(rab)
        self.thread_pool.waitForDone(-1)

        items_info = []
        while not data_queue.empty():
            parent_path, item_path, item = data_queue.get()
            items_info.append((parent_path, item_path, item))
            node_map[item_path] = item
        items_info = sorted(items_info, key=lambda x: x[1])
        for parent_path, item_path, item in items_info:
            parent_item = self._get_parent_item(node_map, parent_path)
            parent_item.addChild(item)

        self.expandAll()
        self.blockSignals(False)
        # 设置列宽策略
        self.setColumnWidth(0, 256)
        self.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(1, 32)
        self.header().setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
        self.setColumnWidth(1, 64)
