from PySide6.QtCore import Slot
from PySide6.QtWidgets import QTableWidget, QHeaderView, QCheckBox, QTableWidgetItem

from utils import byte_size_to_str


class FileTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cellClicked.connect(self.on_cell_clicked)

    def load_table(self, table_datas):
        self.setRowCount(len(table_datas))
        for i, (root, pth, abs_path, is_dir, ext_name, size) in enumerate(table_datas):
            checkbox = QCheckBox()
            checkbox.setChecked(False)
            self.setCellWidget(i, 0, checkbox)
            self.setItem(i, 1, QTableWidgetItem(pth))
            item = QTableWidgetItem(abs_path)
            item.setToolTip(abs_path)
            self.setItem(i, 2, item)
            self.setItem(i, 3, QTableWidgetItem('是' if is_dir else '否'))
            self.setItem(i, 4, QTableWidgetItem(ext_name))
            self.setItem(i, 5, QTableWidgetItem(byte_size_to_str(size)))
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

    def get_checked_path(self):
        delete_datas = []
        for i in range(self.rowCount()):
            checkbox: QCheckBox = self.cellWidget(i, 0)
            if checkbox.isChecked():
                abs_path = self.item(i, 2).text()
                is_dir = self.item(i, 3).text() == '是'
                delete_datas.append((abs_path, is_dir))
        return delete_datas

    def delete_checked(self):
        need_delete_row = []
        for i in range(self.rowCount()):
            checkbox: QCheckBox = self.cellWidget(i, 0)
            if checkbox.isChecked():
                need_delete_row.append(i)
        for i in reversed(need_delete_row):
            self.removeRow(i)

    @Slot()
    def on_cell_clicked(self, row, column):
        if column == 0:
            checkbox: QCheckBox = self.cellWidget(row, column)
            checkbox.setChecked(not checkbox.isChecked())

    @Slot()
    def select_all(self):
        for i in range(self.rowCount()):
            checkbox: QCheckBox = self.cellWidget(i, 0)
            checkbox.setChecked(True)

    @Slot()
    def unselect_all(self):
        for i in range(self.rowCount()):
            checkbox: QCheckBox = self.cellWidget(i, 0)
            checkbox.setChecked(False)
