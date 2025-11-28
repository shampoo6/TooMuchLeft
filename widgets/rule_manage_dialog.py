from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QDialog

from helpers.rule_manager import RuleManager
from uic.rule_manage_dialog import Ui_RuleManageDialog


class RuleManageDialog(QDialog, Ui_RuleManageDialog):
    deletedRules = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.closeButton.clicked.connect(self.close)
        self.deleteButton.clicked.connect(self.on_delete)

        rules = RuleManager.get_instance().rule_data['rules']
        self.ruleNameList.addItems(list(rules.keys()))

    @Slot()
    def on_delete(self):
        idxs = [idx.row() for idx in self.ruleNameList.selectedIndexes()]
        if len(idxs) > 0:
            idxs = sorted(idxs, reverse=True)
            rule_data = RuleManager.get_instance().rule_data
            for idx in idxs:
                item = self.ruleNameList.takeItem(idx)
                text = item.text()
                del rule_data['rules'][text]
                if rule_data['current'] == text:
                    rule_data['current'] = None
            RuleManager.get_instance().update()
            self.deletedRules.emit()
