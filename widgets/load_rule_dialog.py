import os.path

from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox

from constants import base_dir
from uic.load_rule_dialog import Ui_LoadRuleDialog
from helpers.rule_manager import RuleManager


class LoadRuleDialog(QDialog, Ui_LoadRuleDialog):
    ruleLoaded = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.selectFileButton.clicked.connect(self.on_select_file)
        self.closeButton.clicked.connect(self.close)
        self.loadButton.clicked.connect(self.on_load)

    @Slot()
    def on_select_file(self):
        file_path, meta_data = QFileDialog.getOpenFileName(
            self,
            '选择文件',
            base_dir,
            '.txt 或 .gitignore (*.txt *.gitignore)'
        )
        if file_path != '':
            self.ruleFilePathEdit.setText(file_path)

    @Slot()
    def on_load(self):
        rule_name = self.ruleNameEdit.text().strip()
        if rule_name == '':
            QMessageBox.warning(self, '警告', '规则名称不能为空')
            return
        file_path = self.ruleFilePathEdit.text().strip()
        if file_path == '':
            QMessageBox.warning(self, '警告', '规则文件路径不能为空')
            return
        if not os.path.exists(file_path):
            QMessageBox.warning(self, '警告', '规则文件不存在')
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            file_data = f.read()
        lines = file_data.splitlines()
        rules = [line for line in lines if line.strip() != '']
        RuleManager.get_instance().save(rule_name, rules)
        self.ruleLoaded.emit()
        self.close()
