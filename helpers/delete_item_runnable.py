from PySide6.QtCore import QRunnable
from PySide6.QtWidgets import QTreeWidgetItem, QTreeWidget


class DeleteItemRunnable(QRunnable):
    def __init__(self, tree: QTreeWidget, item: QTreeWidgetItem):
        super().__init__()
        self.tree = tree
        self.item = item

    def run(self, /) -> None:
        parent = self.item.parent()
        if parent is not None:
            parent.removeChild(self.item)
        else:
            self.tree.takeTopLevelItem(self.tree.indexOfTopLevelItem(self.item))
