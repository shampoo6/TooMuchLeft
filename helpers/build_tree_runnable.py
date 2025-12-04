import os

from PySide6.QtCore import QRunnable

from utils import create_tree_item


class BuildTreeRunnable(QRunnable):
    # node_map: key: 节点的绝对路径，value: item 对象
    def __init__(self, lock, node_map, tree_data):
        super().__init__()
        self.lock = lock
        self.node_map = node_map
        self.tree_data = tree_data

    def _get_parent_item(self, parent_path):
        with self.lock:
            parent_not_in_map = parent_path not in self.node_map
        if parent_not_in_map:
            pth = parent_path.split(os.sep)[-1]
            parent_item = create_tree_item(pth, parent_path, True, '', '')
            with self.lock:
                self.node_map[parent_path] = parent_item
            parent_parent_path = os.path.abspath(os.path.join(parent_path, '..'))
            parent_parent_item = self._get_parent_item(parent_parent_path)
            parent_parent_item.addChild(parent_item)
        with self.lock:
            parent = self.node_map[parent_path]
        return parent

    def run(self):
        root, pth, abs_path, is_dir, ext_name, size = self.tree_data
        item = create_tree_item(pth, abs_path, is_dir, ext_name, size)
        with self.lock:
            self.node_map[abs_path] = item
        parent_item = self._get_parent_item(root)
        parent_item.addChild(item)
