# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'load_rule_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QToolButton, QVBoxLayout, QWidget)

class Ui_LoadRuleDialog(object):
    def setupUi(self, LoadRuleDialog):
        if not LoadRuleDialog.objectName():
            LoadRuleDialog.setObjectName(u"LoadRuleDialog")
        LoadRuleDialog.resize(238, 108)
        self.formLayout = QFormLayout(LoadRuleDialog)
        self.formLayout.setObjectName(u"formLayout")
        self.label_2 = QLabel(LoadRuleDialog)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.ruleNameEdit = QLineEdit(LoadRuleDialog)
        self.ruleNameEdit.setObjectName(u"ruleNameEdit")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.ruleNameEdit)

        self.label = QLabel(LoadRuleDialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.ruleFilePathEdit = QLineEdit(LoadRuleDialog)
        self.ruleFilePathEdit.setObjectName(u"ruleFilePathEdit")
        self.ruleFilePathEdit.setReadOnly(True)

        self.horizontalLayout.addWidget(self.ruleFilePathEdit)

        self.selectFileButton = QToolButton(LoadRuleDialog)
        self.selectFileButton.setObjectName(u"selectFileButton")

        self.horizontalLayout.addWidget(self.selectFileButton)


        self.formLayout.setLayout(1, QFormLayout.ItemRole.FieldRole, self.horizontalLayout)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_2 = QWidget(LoadRuleDialog)
        self.widget_2.setObjectName(u"widget_2")

        self.verticalLayout.addWidget(self.widget_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.widget = QWidget(LoadRuleDialog)
        self.widget.setObjectName(u"widget")

        self.horizontalLayout_2.addWidget(self.widget)

        self.loadButton = QPushButton(LoadRuleDialog)
        self.loadButton.setObjectName(u"loadButton")

        self.horizontalLayout_2.addWidget(self.loadButton)

        self.closeButton = QPushButton(LoadRuleDialog)
        self.closeButton.setObjectName(u"closeButton")

        self.horizontalLayout_2.addWidget(self.closeButton)

        self.horizontalLayout_2.setStretch(0, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalLayout.setStretch(0, 1)

        self.formLayout.setLayout(2, QFormLayout.ItemRole.FieldRole, self.verticalLayout)


        self.retranslateUi(LoadRuleDialog)

        QMetaObject.connectSlotsByName(LoadRuleDialog)
    # setupUi

    def retranslateUi(self, LoadRuleDialog):
        LoadRuleDialog.setWindowTitle(QCoreApplication.translate("LoadRuleDialog", u"\u52a0\u8f7d\u89c4\u5219", None))
        self.label_2.setText(QCoreApplication.translate("LoadRuleDialog", u"\u89c4\u5219\u540d\u79f0", None))
        self.label.setText(QCoreApplication.translate("LoadRuleDialog", u"\u89c4\u5219\u6587\u4ef6", None))
        self.selectFileButton.setText(QCoreApplication.translate("LoadRuleDialog", u"...", None))
        self.loadButton.setText(QCoreApplication.translate("LoadRuleDialog", u"\u52a0\u8f7d", None))
        self.closeButton.setText(QCoreApplication.translate("LoadRuleDialog", u"\u5173\u95ed", None))
    # retranslateUi

