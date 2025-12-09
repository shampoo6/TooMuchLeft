import os
import sys
import threading
from queue import Queue

import pathspec
from PySide6.QtCore import Slot, Qt, QThreadPool
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog, QMessageBox, QProgressDialog

from helpers.delete_runnable import DeleteRunnable
from helpers.rule_manager import RuleManager, SavedData, RuleData
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
        self.actionQuit.triggered.connect(self.close)

        self.actionSave.setShortcut('Ctrl + S')
        self.actionSaveAs.setShortcut('Ctrl + Shift + S')

        # 规则选择
        RuleManager.get_instance().currentIdChanged.connect(self.update_rule_name_box_and_rule_list)
        self.ruleSpliter.setStretchFactor(0, 2)
        self.ruleSpliter.setStretchFactor(1, 1)
        self.ruleManageButton.clicked.connect(self.on_manage_rules)
        self.ruleNameBox.currentTextChanged.connect(self.on_rule_name_changed)
        self.update_rule_name_box_and_rule_list()

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

        # todo
        self.dir_edit.setText(r'D:\projects\学校\实训')

    def closeEvent(self, e) -> None:
        # 询问是否保存配置
        if self.has_diff_with_saved_data():
            reply = QMessageBox.question(self, '保存', '规则有变化是否保存配置？',
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.on_save()

    def update_rule_name_box(self):
        self.ruleNameBox.blockSignals(True)
        self.ruleNameBox.clear()
        data: SavedData = RuleManager.get_instance().data
        for _id, rule in data['rules'].items():
            self.ruleNameBox.addItem(rule['name'], _id)
        if data['current_id'] is not None:
            self.ruleNameBox.setCurrentText(data['rules'][data['current_id']]['name'])
        self.ruleNameBox.blockSignals(False)

    def update_rule_list(self):
        data: SavedData = RuleManager.get_instance().data
        if data['current_id'] is None:
            return
        current_data = data['rules'][data['current_id']]
        self.includeRuleList.load(current_data['include'])
        self.excludeRuleList.load(current_data['exclude'])

    def get_current_rules(self):
        """获取当前 includeRuleList 和 excludeRuleList 的数据"""
        include_rules = [self.includeRuleList.item(i).text() for i in range(self.includeRuleList.count())]
        exclude_rules = [self.excludeRuleList.item(i).text() for i in range(self.excludeRuleList.count())]
        return include_rules, exclude_rules

    def has_diff_with_saved_data(self):
        include_rules, exclude_rules = self.get_current_rules()
        data: SavedData = RuleManager.get_instance().data
        current_rule = data['rules'][data['current_id']]
        return include_rules != current_rule['include'] or exclude_rules != current_rule['exclude']

    # =================== 槽

    # =================== 工具栏
    @Slot()
    def on_save(self):
        current_id = RuleManager.get_instance().data['current_id']
        if current_id is None:
            self.on_save_as()
        else:
            include_rules, exclude_rules = self.get_current_rules()
            rule_data: RuleData = {
                "name": self.ruleNameBox.currentText(),
                "include": include_rules,
                "exclude": exclude_rules
            }
            _id = self.ruleNameBox.currentData()
            if not RuleManager.get_instance().update_rule(_id, rule_data):
                QMessageBox.critical(self, '保存失败', '找不到对应 _id')

    @Slot()
    def on_save_as(self):
        rule_name, ok = QInputDialog.getText(self, '另存为', '请输入规则名:')
        if not ok:
            return
        include_rules, exclude_rules = self.get_current_rules()
        rule_data: RuleData = {
            "name": rule_name,
            "include": include_rules,
            "exclude": exclude_rules
        }
        if not RuleManager.get_instance().add_rule(rule_data):
            QMessageBox.critical(self, '保存失败', '规则名已存在')
            return
        # 添加规则选项并选中
        if self.ruleNameBox.findText(rule_name) == -1:
            self.ruleNameBox.blockSignals(True)
            self.ruleNameBox.addItem(rule_name, RuleManager.get_instance().data['current_id'])
            self.ruleNameBox.setCurrentText(rule_name)
            self.ruleNameBox.blockSignals(False)

    @Slot()
    def on_load_rule(self):
        self.load_rule_dialog = LoadRuleDialog(self)
        self.load_rule_dialog.open()

    # =================== 规则设置和管理
    @Slot()
    def update_rule_name_box_and_rule_list(self):
        """当前规则发生变化时，更新视图"""
        self.update_rule_name_box()
        self.update_rule_list()

    @Slot()
    def on_rule_name_changed(self, text):
        if isinstance(text, str) and text.strip() != '':
            rule_id = self.ruleNameBox.currentData()
            RuleManager.get_instance().switch_rule(rule_id)

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
        self.rule_manage_dialog.open()

    @Slot()
    def on_search(self):
        dir_path = self.dir_edit.text()
        if dir_path == '':
            QMessageBox.warning(self, '警告', '请选择一个搜索目录')
            return
        if not os.path.exists(dir_path):
            QMessageBox.critical(self, '错误', '目录不存在')
            return

        include_rules, exclude_rules = self.get_current_rules()
        include_spec = pathspec.PathSpec.from_lines('gitwildmatch', include_rules) if len(include_rules) > 0 else None
        exclude_spec = pathspec.PathSpec.from_lines('gitwildmatch', exclude_rules) if len(exclude_rules) > 0 else None

        data_queue = Queue()
        rab = SearchRunnable(data_queue, include_spec, exclude_spec, dir_path, self.compareBox.currentText(),
                             self.sizeBox.currentText())
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
