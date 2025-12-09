from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QDialog, QListWidgetItem, QMessageBox

from helpers.rule_manager import RuleManager, SavedData
from uic.rule_manage_dialog import Ui_RuleManageDialog


class RuleManageDialog(QDialog, Ui_RuleManageDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.closeButton.clicked.connect(self.close)
        self.deleteButton.clicked.connect(self.on_delete)

        data: SavedData = RuleManager.get_instance().data
        for _id, rule in data['rules'].items():
            item = QListWidgetItem(rule['name'])
            item.setData(Qt.ItemDataRole.UserRole, _id)
            self.ruleNameList.addItem(item)

    @Slot()
    def on_delete(self):
        idxs = [idx.row() for idx in self.ruleNameList.selectedIndexes()]
        if len(idxs) > 0:
            idxs = sorted(idxs, reverse=True)
            _ids = []
            for idx in idxs:
                item = self.ruleNameList.takeItem(idx)
                _id = item.data(Qt.ItemDataRole.UserRole)
                _ids.append(_id)
            if not RuleManager.get_instance().delete_rule(_ids):
                QMessageBox.critical(self.parent, '错误', 'id 不存在无法删除')
