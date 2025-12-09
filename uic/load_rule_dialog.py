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
        LoadRuleDialog.resize(236, 106)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LoadRuleDialog.sizePolicy().hasHeightForWidth())
        LoadRuleDialog.setSizePolicy(sizePolicy)
        LoadRuleDialog.setMaximumSize(QSize(236, 106))
        self.formLayout = QFormLayout(LoadRuleDialog)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(LoadRuleDialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.ruleFilePathEdit = QLineEdit(LoadRuleDialog)
        self.ruleFilePathEdit.setObjectName(u"ruleFilePathEdit")
        self.ruleFilePathEdit.setReadOnly(True)

        self.horizontalLayout.addWidget(self.ruleFilePathEdit)

        self.selectFileButton = QToolButton(LoadRuleDialog)
        self.selectFileButton.setObjectName(u"selectFileButton")

        self.horizontalLayout.addWidget(self.selectFileButton)


        self.formLayout.setLayout(0, QFormLayout.ItemRole.FieldRole, self.horizontalLayout)

        self.viewTemplateButton = QPushButton(LoadRuleDialog)
        self.viewTemplateButton.setObjectName(u"viewTemplateButton")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.viewTemplateButton)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.loadButton = QPushButton(LoadRuleDialog)
        self.loadButton.setObjectName(u"loadButton")

        self.horizontalLayout_2.addWidget(self.loadButton)

        self.closeButton = QPushButton(LoadRuleDialog)
        self.closeButton.setObjectName(u"closeButton")

        self.horizontalLayout_2.addWidget(self.closeButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.formLayout.setLayout(2, QFormLayout.ItemRole.FieldRole, self.verticalLayout)


        self.retranslateUi(LoadRuleDialog)

        QMetaObject.connectSlotsByName(LoadRuleDialog)
    # setupUi

    def retranslateUi(self, LoadRuleDialog):
        LoadRuleDialog.setWindowTitle(QCoreApplication.translate("LoadRuleDialog", u"\u52a0\u8f7d\u89c4\u5219", None))
        self.label.setText(QCoreApplication.translate("LoadRuleDialog", u"\u89c4\u5219\u6587\u4ef6", None))
        self.selectFileButton.setText(QCoreApplication.translate("LoadRuleDialog", u"...", None))
        self.viewTemplateButton.setText(QCoreApplication.translate("LoadRuleDialog", u"\u67e5\u770b\u89c4\u5219\u6587\u4ef6\u6a21\u677f", None))
        self.loadButton.setText(QCoreApplication.translate("LoadRuleDialog", u"\u52a0\u8f7d", None))
        self.closeButton.setText(QCoreApplication.translate("LoadRuleDialog", u"\u5173\u95ed", None))
    # retranslateUi

