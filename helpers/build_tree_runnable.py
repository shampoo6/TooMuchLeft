import os

from PySide6.QtCore import QRunnable, Qt
from PySide6.QtWidgets import QTreeWidgetItem

from utils import byte_size_to_str, create_tree_item
from constants import PathType


class BuildTreeRunnable(QRunnable):
    def __init__(self, data_queue, tree_data):
        super().__init__()
        self.data_queue = data_queue
        self.tree_data = tree_data

    def run(self):
        root, pth, abs_path, is_dir, ext_name, size = self.tree_data
        item = create_tree_item(pth, abs_path, is_dir, ext_name, size)
        self.data_queue.put((root, abs_path, item))
