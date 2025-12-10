import os
import subprocess

from PySide6.QtCore import Slot, QTimer, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QTableWidget, QHeaderView, QCheckBox, QTableWidgetItem, QMenu, QApplication

from utils import byte_size_to_str


class FileTable(QTableWidget):
    # 表格加载完成
    loaded = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cancel_event = None
        # 第一批显示数据的大小
        self.first_batch_size = 1000
        self.batch_size = 3
        self.cellClicked.connect(self.on_cell_clicked)

    def contextMenuEvent(self, e) -> None:
        p = e.pos()
        row_idx = self.rowAt(p.y())
        if row_idx != -1:
            context = QMenu(self)
            open_dir_action = QAction('打开文件夹', self)
            copy_action = QAction('复制路径', self)

            @Slot()
            def _open_file_dir():
                pth = self.item(row_idx, 2).text()
                if self.item(row_idx, 3).text() == '否':
                    # 选中文件
                    subprocess.run(f'explorer /select,"{pth}"', shell=True)
                else:
                    os.startfile(pth)

            @Slot()
            def _copy_path():
                pth = self.item(row_idx, 2).text()
                QApplication.clipboard().setText(pth)

            open_dir_action.triggered.connect(_open_file_dir)
            copy_action.triggered.connect(_copy_path)
            context.addAction(open_dir_action)
            context.addAction(copy_action)
            context.exec(e.globalPos())

    def _build_table(self, table_datas):
        for root, pth, abs_path, is_dir, ext_name, size in table_datas:
            i = self.rowCount()
            self.insertRow(i)
            abs_path = os.path.normpath(abs_path)
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

    def _build_next_batch(self, batch_idx, table_datas):
        if self.cancel_event.is_set():
            self.loaded.emit()
            return
        start_i = batch_idx.pop(0)
        _table_datas = table_datas[start_i:start_i + self.batch_size]
        self._build_table(_table_datas)
        if len(batch_idx) > 0:
            QTimer.singleShot(0, lambda: self._build_next_batch(batch_idx, table_datas))
        else:
            self.loaded.emit()

    def _build_first_batch(self, table_datas):
        if self.cancel_event.is_set():
            self.loaded.emit()
            return
        row_count = len(table_datas)

        # 先批量构造一批结果
        _first_batch_count = row_count if row_count <= self.first_batch_size else self.first_batch_size
        _first_batch_datas = table_datas[:_first_batch_count]

        self._build_table(_first_batch_datas)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

        if self.cancel_event.is_set():
            self.loaded.emit()
            return

        if row_count > self.first_batch_size:
            # 分批加载
            row_count -= self.first_batch_size
            table_datas = table_datas[_first_batch_count:]
            batch_idx = [i for i in range(0, row_count, self.batch_size)]
            self._build_next_batch(batch_idx, table_datas)
        else:
            self.loaded.emit()

    def load_table(self, cancel_event, table_datas):
        self.cancel_event = cancel_event
        self.clearContents()
        self.setRowCount(0)

        if self.cancel_event.is_set():
            self.loaded.emit()
            return

        if len(table_datas) == 0:
            return

        QTimer.singleShot(0, lambda: self._build_first_batch(table_datas))

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
