from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemDelegate


class EditableList(QListWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_edit_item = None
        delegate = self.itemDelegate()
        delegate.closeEditor.connect(self.on_editor_closed)

    def load(self, items):
        self.clear()
        for item in items:
            item = QListWidgetItem(item)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.addItem(item)

    @Slot()
    def add_new_rule(self):
        item = QListWidgetItem('')
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
        self.addItem(item)
        self.editItem(item)
        self.current_edit_item = item
        return item

    @Slot()
    def delete_rules(self):
        idxs =[idx.row() for idx in self.selectedIndexes()]
        if len(idxs) > 0:
            idxs = sorted(idxs, reverse=True)
            for idx in idxs:
                self.takeItem(idx)

    def mouseDoubleClickEvent(self, e) -> None:
        item = self.itemAt(e.pos())
        if item is None:
            self.add_new_rule()
        else:
            self.editItem(item)
            self.current_edit_item = item

    def on_editor_closed(self, editor, hint):
        if self.current_edit_item is None:
            return

        if editor.text().strip() == '':
            self.takeItem(self.row(self.current_edit_item))

        self.current_edit_item = None
