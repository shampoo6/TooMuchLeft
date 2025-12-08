import os

from PySide6.QtCore import QRunnable
from PySide6.QtWidgets import QCheckBox, QTableWidgetItem

from utils import byte_size_to_str


class BuildItemRunnable(QRunnable):
    def __init__(self, queue, i, table_data):
        super().__init__()
        self.queue = queue
        self.i = i
        self.table_data = table_data

    def run(self, /) -> None:
        root, pth, abs_path, is_dir, ext_name, size = self.table_data
        abs_path = os.path.normpath(abs_path)
        checkbox = QCheckBox()
        checkbox.setChecked(False)
        name_item = QTableWidgetItem(pth)
        abs_path_item = QTableWidgetItem(abs_path)
        abs_path_item.setToolTip(abs_path)
        is_dir_item = QTableWidgetItem('是' if is_dir else '否')
        ext_name_item = QTableWidgetItem(ext_name)
        size_item = QTableWidgetItem(byte_size_to_str(size))
        self.queue.put((self.i, (checkbox, name_item, abs_path_item, is_dir_item, ext_name_item, size_item)))
