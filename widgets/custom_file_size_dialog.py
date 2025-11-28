from PySide6.QtWidgets import QDialog
from uic.custom_file_size_dialog import Ui_CustomFileSizeDialog


class CustomFileSizeDialog(QDialog, Ui_CustomFileSizeDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.unitBox.setCurrentText('MB')
