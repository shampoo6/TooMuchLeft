import os
import subprocess

from PySide6.QtCore import Slot, QTimer, Signal, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QTableWidget, QHeaderView, QCheckBox, QTableWidgetItem, QMenu, QApplication, QStyle

from utils import byte_size_to_str, file_size_to_byte


class FileTable(QTableWidget):
    # 表格加载完成，True 代表加载完成 False 代表取消
    loaded = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cancel_event = None
        # 第一批显示数据的大小
        self.first_batch_size = 1000
        self.batch_size = 3
        self.cellClicked.connect(self.on_cell_clicked)
        
        # 存储原始数据用于排序
        self.original_data = []
        # 当前列排序状态 (列索引, 排序顺序)
        self.sort_column = -1
        self.sort_order = Qt.AscendingOrder
        # 排序功能开关，只有在表格加载完成后才能使用
        self.sort_enabled = False
        
        # 启用表头排序
        self.horizontalHeader().setSectionsClickable(True)
        self.horizontalHeader().sectionClicked.connect(self.on_header_clicked)
        
        # 获取排序指示器图标
        self.style = QApplication.style()
        self.sort_ascending_icon = self.style.standardIcon(QStyle.SP_ArrowUp)
        self.sort_descending_icon = self.style.standardIcon(QStyle.SP_ArrowDown)
        
        # 设置表头样式，将排序指示器放在右侧
        self.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                /*padding-right: 20px;   为排序指示器留出空间 */
                text-align: left;
                border: 1px solid #c0c0c0;
                background-color: #f0f0f0;
            }
            QHeaderView::down-arrow {
                image: url(:/icons/arrow-down-bold.png);
                subcontrol-position: right;
                right: 5px;
                width: 12px;
                height: 12px;
            }
            QHeaderView::up-arrow {
                image: url(:/icons/arrow-up-bold.png);
                subcontrol-position: right;
                right: 5px;
                width: 12px;
                height: 12px;
            }
        """)

    def contextMenuEvent(self, e) -> None:
        p = e.pos()
        row_idx = self.rowAt(p.y())
        if row_idx != -1:
            context = QMenu(self)
            open_dir_action = QAction('打开文件夹', self)
            copy_action = QAction('复制路径', self)
            remove_action = QAction('移除选择项', self)

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

            @Slot()
            def _remove_rows():
                indices = [i.row() for i in self.selectedIndexes()]
                if len(indices) > 0:
                    indices = sorted(indices, reverse=True)
                    for i in indices:
                        self.removeRow(i)

            open_dir_action.triggered.connect(_open_file_dir)
            copy_action.triggered.connect(_copy_path)
            remove_action.triggered.connect(_remove_rows)
            context.addAction(open_dir_action)
            context.addAction(copy_action)
            context.addAction(remove_action)
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
            self.loaded.emit(False)
            return
        start_i = batch_idx.pop(0)
        _table_datas = table_datas[start_i:start_i + self.batch_size]
        self._build_table(_table_datas)
        if len(batch_idx) > 0:
            QTimer.singleShot(0, lambda: self._build_next_batch(batch_idx, table_datas))
        else:
            # 表格加载完成，启用排序功能
            self.sort_enabled = True
            self.loaded.emit(True)

    def _build_first_batch(self, table_datas):
        if self.cancel_event.is_set():
            self.loaded.emit(False)
            return
        row_count = len(table_datas)

        # 先批量构造一批结果
        _first_batch_count = row_count if row_count <= self.first_batch_size else self.first_batch_size
        _first_batch_datas = table_datas[:_first_batch_count]

        self._build_table(_first_batch_datas)
        
        # 设置表头标签
        self.setHorizontalHeaderLabels(['', '相对路径', '绝对路径', '是否目录', '扩展名', '大小'])
        
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

        if self.cancel_event.is_set():
            self.loaded.emit(False)
            return

        if row_count > self.first_batch_size:
            # 分批加载
            row_count -= self.first_batch_size
            table_datas = table_datas[_first_batch_count:]
            batch_idx = [i for i in range(0, row_count, self.batch_size)]
            self._build_next_batch(batch_idx, table_datas)
        else:
            # 表格加载完成，启用排序功能
            self.sort_enabled = True
            self.loaded.emit(True)

    def load_table(self, cancel_event, table_datas):
        self.cancel_event = cancel_event
        self.clearContents()
        self.setRowCount(0)
        
        # 关闭排序功能
        self.sort_enabled = False
        
        # 保存原始数据用于排序
        self.original_data = table_datas.copy()
        # 重置排序状态
        self.sort_column = -1
        self.sort_order = Qt.AscendingOrder
        # 清除排序指示器
        self._update_sort_indicator()

        if self.cancel_event.is_set():
            self.loaded.emit(False)
            return

        if len(table_datas) == 0:
            self.loaded.emit(True)
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
    
    @Slot(int)
    def on_header_clicked(self, column):
        """处理表头点击事件，实现排序功能"""
        # 检查排序功能是否启用
        if not self.sort_enabled:
            return
            
        # 复选框列不排序
        if column == 0:
            return
            
        # 如果点击的是同一列，则切换排序顺序
        if self.sort_column == column:
            self.sort_order = Qt.DescendingOrder if self.sort_order == Qt.AscendingOrder else Qt.AscendingOrder
        else:
            self.sort_column = column
            self.sort_order = Qt.AscendingOrder
        
        # 对原始数据进行排序
        sorted_data = self._sort_data(self.original_data, column, self.sort_order)
        
        # 重新加载表格
        self._reload_table(sorted_data)
    
    def _sort_data(self, data, column, order):
        """根据列和排序顺序对数据进行排序"""
        reverse = (order == Qt.DescendingOrder)
        
        if column == 1:  # 相对路径列
            return sorted(data, key=lambda x: x[1], reverse=reverse)
        elif column == 2:  # 绝对路径列
            return sorted(data, key=lambda x: x[2], reverse=reverse)
        elif column == 3:  # 是否目录列
            return sorted(data, key=lambda x: x[3], reverse=reverse)
        elif column == 4:  # 扩展名列
            return sorted(data, key=lambda x: x[4], reverse=reverse)
        elif column == 5:  # 大小列
            return sorted(data, key=lambda x: x[5], reverse=reverse)
        else:
            return data
    
    def _reload_table(self, sorted_data):
        """重新加载表格数据"""
        # 保存当前选中状态
        checked_items = set()
        for i in range(self.rowCount()):
            checkbox: QCheckBox = self.cellWidget(i, 0)
            if checkbox.isChecked():
                abs_path = self.item(i, 2).text()
                checked_items.add(abs_path)
        
        # 清空表格
        self.clearContents()
        self.setRowCount(0)
        
        # 重新构建表格
        self._build_table(sorted_data)
        
        # 设置表头标签
        self.setHorizontalHeaderLabels(['', '相对路径', '绝对路径', '是否目录', '扩展名', '大小'])
        
        # 恢复选中状态
        for i in range(self.rowCount()):
            abs_path = self.item(i, 2).text()
            if abs_path in checked_items:
                checkbox: QCheckBox = self.cellWidget(i, 0)
                checkbox.setChecked(True)
        
        # 更新列宽
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        
        # 更新排序指示器
        self._update_sort_indicator()
    
    def _update_sort_indicator(self):
        """更新表头排序指示器"""
        header = self.horizontalHeader()
        
        # 确保表头可点击
        header.setSectionsClickable(True)
        
        # 如果有排序列，显示排序指示器
        if self.sort_column >= 0:
            header.setSortIndicator(self.sort_column, self.sort_order)
            # 确保显示排序指示器
            header.setSortIndicatorShown(True)
        else:
            # 隐藏排序指示器
            header.setSortIndicatorShown(False)
