import ctypes
import os
import subprocess
import threading

from PySide6.QtCore import Qt, Slot, QThreadPool
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QHeaderView, QMenu

from helpers.build_tree_runnable import BuildTreeRunnable
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
            self._sync_child_check_state(item, item.checkState(0))
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
    def _sync_child_check_state(self, parent: QTreeWidgetItem, check_state: Qt.CheckState):
        for i in range(parent.childCount()):
            child = parent.child(i)
            child.setCheckState(0, check_state)
            self._sync_child_check_state(child, check_state)
            if child.childCount() > 0:
                self._sync_child_check_state(child, check_state)

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

    def load_tree(self, search_tgt_dir, tree_node_queue):
        self.blockSignals(True)
        self.clear()

        node_map = {
            search_tgt_dir: self.invisibleRootItem()
        }

        def _build_node():
            lock = threading.Lock()
            while 1:
                tree_data = tree_node_queue.get()
                rab = BuildTreeRunnable(lock, node_map, tree_data)
                self.thread_pool.start(rab)

        thread = threading.Thread(target=_build_node)
        thread.start()
        self.thread_pool.waitForDone(-1)
        # 强制删除线程
        thread_id = thread.ident
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        # 展开
        self.expandAll()
        self.blockSignals(False)
        # 设置列宽策略
        self.setColumnWidth(0, 256)
        self.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(1, 32)
        self.header().setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
        self.setColumnWidth(1, 64)
