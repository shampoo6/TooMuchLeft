import os
import sys
import threading
from queue import Queue

import pathspec
from PySide6.QtCore import Slot, Qt, QThreadPool
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog, QMessageBox, QProgressDialog

from helpers.delete_runnable import DeleteRunnable
from helpers.rule_manager import RuleManager
from helpers.search_runnable import SearchRunnable
from uic.main_table_widget import Ui_MainWindow
from widgets.custom_file_size_dialog import CustomFileSizeDialog
from constants import base_dir
from widgets.load_rule_dialog import LoadRuleDialog
from widgets.rule_manage_dialog import RuleManageDialog


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('删不尽')

        self.thread_pool = QThreadPool.globalInstance()
        self.custom_file_size_dialog = None
        self.rule_manage_dialog = None
        self.load_rule_dialog = None

        # 工具栏
        self.actionSave.triggered.connect(self.on_save)
        self.actionSaveAs.triggered.connect(self.on_save_as)
        self.actionLoad.triggered.connect(self.on_load_rule)
        self.actionAdd.triggered.connect(self.ruleList.add_new_rule)
        self.actionDelete.triggered.connect(self.ruleList.delete_rules)
        self.actionQuit.triggered.connect(self.close)

        self.actionSave.setShortcut('Ctrl + S')
        self.actionSaveAs.setShortcut('Ctrl + Shift + S')

        # 规则选择
        self.ruleManageButton.clicked.connect(self.on_manage_rules)
        self.ruleNameBox.currentTextChanged.connect(self.on_rule_name_changed)
        self.update_rule_name_box()
        self.on_rule_name_changed(self.ruleNameBox.currentText())

        # 目录选择
        self.selectDirButton.clicked.connect(self.on_select_dir)

        # 文件大小选择
        self.moreSizeButton.clicked.connect(self.on_more_size)

        # 搜索按钮
        self.searchButton.clicked.connect(self.on_search)
        self.searchButton.setShortcut('Ctrl + Return')

        # 文件列表
        self.selectAllButton.clicked.connect(self.fileTable.select_all)
        self.unselectAllButton.clicked.connect(self.fileTable.unselect_all)
        self.deleteButton.clicked.connect(self.on_delete)
        self.deleteButton.setShortcut('Ctrl + D')

    def closeEvent(self, e) -> None:
        # 询问是否保存配置
        current = RuleManager.get_instance().rule_data['current']
        if current is not None:
            # 对比深度相等
            deep_equal = True
            current_data = RuleManager.get_instance().rule_data['rules'][current]
            rules = [self.ruleList.item(i).text() for i in range(self.ruleList.count())]
            if len(current_data) != len(rules):
                deep_equal = False
            if deep_equal:
                for i in range(len(current_data)):
                    if current_data[i] != rules[i]:
                        deep_equal = False
                        break
            if not deep_equal:
                reply = QMessageBox.question(self, '保存', '规则有变化是否保存配置？',
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.Yes:
                    self.on_save()

    @Slot()
    def update_rule_name_box(self):
        last_rule_name = self.ruleNameBox.currentText()

        self.ruleNameBox.blockSignals(True)
        self.ruleNameBox.clear()
        rule_data = RuleManager.get_instance().rule_data
        for rule_name in rule_data['rules'].keys():
            self.ruleNameBox.addItem(rule_name)
        self.ruleNameBox.blockSignals(False)

        if last_rule_name != rule_data['current']:
            self.ruleNameBox.setCurrentText(rule_data['current'])

    # =================== 槽

    # =================== 工具栏
    @Slot()
    def on_save(self):
        current = RuleManager.get_instance().rule_data['current']
        if current is None:
            self.on_save_as()
        else:
            rules = [self.ruleList.item(i).text() for i in range(self.ruleList.count())]
            RuleManager.get_instance().save(current, rules)

    @Slot()
    def on_save_as(self):
        rule_name, ok = QInputDialog.getText(self, '另存为', '请输入规则名:')
        if not ok:
            return
        rules = [self.ruleList.item(i).text() for i in range(self.ruleList.count())]
        RuleManager.get_instance().save(rule_name, rules)
        # 添加规则选项并选中
        if self.ruleNameBox.findText(rule_name) == -1:
            self.ruleNameBox.addItem(rule_name)
            self.ruleNameBox.setCurrentText(rule_name)

    @Slot()
    def on_load_rule(self):
        self.load_rule_dialog = LoadRuleDialog(self)
        self.load_rule_dialog.ruleLoaded.connect(self.update_rule_name_box)
        self.load_rule_dialog.open()

    # =================== 规则设置和管理
    @Slot()
    def on_rule_name_changed(self, text):
        if isinstance(text, str) and text.strip() != '':
            rd = RuleManager.get_instance().rule_data
            RuleManager.get_instance().setCurrent(text)
            rule_items = rd['rules'][text]
            self.ruleList.load(rule_items)

    @Slot()
    def on_select_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, '选择目录',
                                                    base_dir if self.dir_edit.text() == '' else self.dir_edit.text())
        if dir_path != '':
            self.dir_edit.setText(dir_path)

    @Slot()
    def on_more_size(self):
        self.custom_file_size_dialog = CustomFileSizeDialog(self)
        self.custom_file_size_dialog.accepted.connect(self.on_custom_file_size_dialog_confirm)
        self.custom_file_size_dialog.open()

    @Slot()
    def on_custom_file_size_dialog_confirm(self):
        size = self.custom_file_size_dialog.sizeBox.value()
        unit = self.custom_file_size_dialog.unitBox.currentText()
        self.sizeBox.addItem(f"{size}{unit}")
        self.sizeBox.setCurrentText(f"{size}{unit}")

    @Slot()
    def on_manage_rules(self):
        self.rule_manage_dialog = RuleManageDialog()
        self.rule_manage_dialog.deletedRules.connect(self.update_rule_name_box_and_clear_rule_list)
        self.rule_manage_dialog.open()

    @Slot()
    def update_rule_name_box_and_clear_rule_list(self):
        self.update_rule_name_box()
        if RuleManager.get_instance().rule_data['current'] is None:
            self.ruleList.clear()

    @Slot()
    def on_search(self):
        dir_path = self.dir_edit.text()
        if dir_path == '':
            QMessageBox.warning(self, '警告', '请选择一个搜索目录')
            return
        if not os.path.exists(dir_path):
            QMessageBox.critical(self, '错误', '目录不存在')
            return
        rules = [self.ruleList.item(i).text() for i in range(self.ruleList.count())]
        if len(rules) == 0:
            # 没有过滤条件，则匹配所有内容
            spec = pathspec.PathSpec.from_lines('gitwildmatch', ['**'])
        else:
            spec = pathspec.PathSpec.from_lines('gitwildmatch', rules)

        data_queue = Queue()
        rab = SearchRunnable(data_queue, spec, dir_path, self.compareBox.currentText(), self.sizeBox.currentText())
        self.thread_pool.start(rab)
        self.thread_pool.waitForDone(-1)
        # 构建表格
        table_datas = []
        while not data_queue.empty():
            table_datas.append(data_queue.get())
        table_datas = sorted(table_datas, key=lambda x: x[2])
        self.fileTable.load_table(table_datas)

    # =================== 删除
    @Slot()
    def on_delete(self):
        # 搜集所有勾选项
        delete_datas = self.fileTable.get_checked_path()
        total_step = len(delete_datas)
        if total_step == 0:
            return
        # 增加一步，用于删除 ui 界面中的选项
        total_step += 1

        result = QMessageBox.question(self, '删除', '确定删除吗？',
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                      QMessageBox.StandardButton.No)
        if result == QMessageBox.StandardButton.No:
            return
        current_step = 0

        progress = QProgressDialog("删除中...", "取消", 0, total_step,
                                   self) if self.disableProgressCheckBox.checkState() == Qt.CheckState.Unchecked else None
        if progress is not None:
            progress.setWindowTitle('删除')
            progress.setWindowModality(Qt.WindowModality.WindowModal)
            progress.setMinimumWidth(200)
            progress.setMaximumWidth(300)
            progress.show()

        queue = Queue() if progress is not None else None
        cancel_event = threading.Event() if progress is not None else None
        for abs_path, is_dir in delete_datas:
            rab = DeleteRunnable(abs_path, is_dir, queue, cancel_event)
            self.thread_pool.start(rab)
        if progress is not None:
            while current_step < total_step - 1:
                if progress.wasCanceled():
                    cancel_event.set()
                    break
                deleted_path = queue.get()
                current_step += 1
                progress.setLabelText(f'已删除: {os.path.basename(deleted_path)}')
                progress.setValue(current_step)

        self.thread_pool.waitForDone(-1)
        # 更新 ui
        self.fileTable.delete_checked()
        if progress is not None:
            current_step += 1
            progress.setLabelText(f'删除完毕')
            progress.setValue(current_step)


app = QApplication(sys.argv)
app.setWindowIcon(QIcon(os.path.join(base_dir, 'icon.ico')))

window = MainWindow()
window.show()

app.exec()
