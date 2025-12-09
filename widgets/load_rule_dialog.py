import json
import os.path

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox

from constants import base_dir
from uic.load_rule_dialog import Ui_LoadRuleDialog
from helpers.rule_manager import RuleManager, RuleData


class LoadRuleDialog(QDialog, Ui_LoadRuleDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.selectFileButton.clicked.connect(self.on_select_file)
        self.viewTemplateButton.clicked.connect(self.on_view_template)
        self.closeButton.clicked.connect(self.close)
        self.loadButton.clicked.connect(self.on_load)

    @Slot()
    def on_select_file(self):
        file_path, meta_data = QFileDialog.getOpenFileName(
            self,
            '选择文件',
            base_dir,
            '.txt 或 .json (*.txt *.json)'
        )
        if file_path != '':
            self.ruleFilePathEdit.setText(file_path)

    @Slot()
    def on_view_template(self):
        file_path = os.path.join(base_dir, 'rule_template.txt')
        os.startfile(file_path)

    @Slot()
    def on_load(self):
        file_path = self.ruleFilePathEdit.text().strip()
        if file_path == '':
            QMessageBox.warning(self, '警告', '规则文件路径不能为空')
            return
        if not os.path.exists(file_path):
            QMessageBox.warning(self, '警告', '规则文件不存在')
            return
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data: RuleData = json.load(f)
        except:
            QMessageBox.warning(self, '警告', '规则文件格式错误')
            return
        # 校验 data 数据
        if 'name' not in data:
            QMessageBox.warning(self, '警告', 'name 字段不能为空')
            return
        if 'include' not in data or not isinstance(data['include'], list):
            QMessageBox.warning(self, '警告', 'include 字段不能为空且必须为列表')
            return
        if 'exclude' not in data or not isinstance(data['exclude'], list):
            QMessageBox.warning(self, '警告', 'exclude 字段不能为空且必须为列表')
            return
        if not RuleManager.get_instance().add_rule(data):
            QMessageBox.warning(self, '警告', '规则名已存在')
            return
        self.close()
