import enum
import os
import subprocess

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QHeaderView, QMenu

from utils import path_analysis, byte_size_to_str


class FileTree(QTreeWidget):
    class PathType(enum.Enum):
        DIR = 0
        FILE = 1

    def __init__(self, parent=None):
        super().__init__(parent)
        self.itemChanged.connect(self.on_item_changed)

    def contextMenuEvent(self, e) -> None:
        item = self.itemAt(e.pos())
        if item is not None:
            context = QMenu(self)
            open_dir_action = QAction('打开文件夹', self)

            @Slot()
            def _open_file_dir():
                if item.data(0, Qt.ItemDataRole.UserRole) == FileTree.PathType.FILE:
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
        if item.data(0, Qt.ItemDataRole.UserRole) == FileTree.PathType.DIR:
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

    def _get_dir_item(self, parent, dirs, root_path):
        if len(dirs) == 0:
            return parent
        dir_name = dirs.pop(0)
        current_item = None
        for i in range(parent.childCount()):
            child = parent.child(i)
            child_name = child.text(0)  # 第一列固定为名称
            if child_name == dir_name:
                current_item = child
                break
        if current_item is None:
            current_item = QTreeWidgetItem(parent)
            # 设置路径类型，是目录还是文件
            current_item.setData(0, Qt.ItemDataRole.UserRole, FileTree.PathType.DIR)
            current_item.setText(0, dir_name)
            current_item.setFlags(current_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            current_item.setCheckState(0, Qt.CheckState.Checked)
            # 设置tooltip
            parent_path = parent.toolTip(0) or root_path
            current_item.setToolTip(0, os.path.normpath(os.path.join(parent_path, dir_name)))
            parent.addChild(current_item)
        if len(dirs) > 0:
            return self._get_dir_item(current_item, dirs, root_path)
        else:
            return current_item

    def load_file_tree(self, file_datas, root_path):
        """
        加载文件树
        :param file_datas: 文件数据
        :param root_path: 搜索根路径
        :return:
        """
        self.blockSignals(True)
        self.clear()
        root = self.invisibleRootItem()
        for file_data in file_datas:
            file_path, match, ext_name, file_size = file_data
            path_slice = path_analysis(match)
            dirs = path_slice[:-1]
            file_name = path_slice[-1]
            # 查找目录节点
            dir_item = self._get_dir_item(root, dirs, root_path)
            # 创建文件节点
            file_item = QTreeWidgetItem(dir_item)
            file_item.setText(0, file_name)
            file_item.setText(1, ext_name)
            file_item.setText(2, byte_size_to_str(file_size))
            file_item.setFlags(file_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            file_item.setCheckState(0, Qt.CheckState.Checked)
            file_item.setToolTip(0, file_path)
            # 设置路径类型
            file_item.setData(0, Qt.ItemDataRole.UserRole, FileTree.PathType.FILE)
            dir_item.addChild(file_item)
        self.expandAll()
        self.blockSignals(False)
        # 设置列宽策略
        self.setColumnWidth(0, 256)
        self.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(1, 32)
        self.header().setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
        self.setColumnWidth(1, 64)

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
            if path_type == FileTree.PathType.FILE and current_item.checkState(0) == Qt.CheckState.Checked:
                file_items.append(current_item)
            elif path_type == FileTree.PathType.DIR and current_item.checkState(0) == Qt.CheckState.Checked:
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
