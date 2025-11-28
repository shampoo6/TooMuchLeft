# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'custom_file_size_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFormLayout, QLabel, QSizePolicy,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_CustomFileSizeDialog(object):
    def setupUi(self, CustomFileSizeDialog):
        if not CustomFileSizeDialog.objectName():
            CustomFileSizeDialog.setObjectName(u"CustomFileSizeDialog")
        CustomFileSizeDialog.resize(174, 97)
        CustomFileSizeDialog.setMinimumSize(QSize(174, 97))
        self.verticalLayout = QVBoxLayout(CustomFileSizeDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(CustomFileSizeDialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.sizeBox = QSpinBox(CustomFileSizeDialog)
        self.sizeBox.setObjectName(u"sizeBox")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.sizeBox)

        self.label_2 = QLabel(CustomFileSizeDialog)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.unitBox = QComboBox(CustomFileSizeDialog)
        self.unitBox.addItem("")
        self.unitBox.addItem("")
        self.unitBox.addItem("")
        self.unitBox.addItem("")
        self.unitBox.addItem("")
        self.unitBox.setObjectName(u"unitBox")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.unitBox)


        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(CustomFileSizeDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(CustomFileSizeDialog)
        self.buttonBox.accepted.connect(CustomFileSizeDialog.accept)
        self.buttonBox.rejected.connect(CustomFileSizeDialog.reject)

        QMetaObject.connectSlotsByName(CustomFileSizeDialog)
    # setupUi

    def retranslateUi(self, CustomFileSizeDialog):
        CustomFileSizeDialog.setWindowTitle(QCoreApplication.translate("CustomFileSizeDialog", u"\u81ea\u5b9a\u4e49\u6587\u4ef6\u5927\u5c0f", None))
        self.label.setText(QCoreApplication.translate("CustomFileSizeDialog", u"\u6587\u4ef6\u5927\u5c0f", None))
        self.label_2.setText(QCoreApplication.translate("CustomFileSizeDialog", u"\u5355\u4f4d", None))
        self.unitBox.setItemText(0, QCoreApplication.translate("CustomFileSizeDialog", u"B", None))
        self.unitBox.setItemText(1, QCoreApplication.translate("CustomFileSizeDialog", u"KB", None))
        self.unitBox.setItemText(2, QCoreApplication.translate("CustomFileSizeDialog", u"MB", None))
        self.unitBox.setItemText(3, QCoreApplication.translate("CustomFileSizeDialog", u"GB", None))
        self.unitBox.setItemText(4, QCoreApplication.translate("CustomFileSizeDialog", u"TB", None))

    # retranslateUi

