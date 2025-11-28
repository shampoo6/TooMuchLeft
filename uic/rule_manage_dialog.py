# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rule_manage_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QHBoxLayout,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_RuleManageDialog(object):
    def setupUi(self, RuleManageDialog):
        if not RuleManageDialog.objectName():
            RuleManageDialog.setObjectName(u"RuleManageDialog")
        RuleManageDialog.resize(213, 175)
        RuleManageDialog.setMinimumSize(QSize(213, 175))
        self.verticalLayout = QVBoxLayout(RuleManageDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.ruleNameList = QListWidget(RuleManageDialog)
        self.ruleNameList.setObjectName(u"ruleNameList")
        self.ruleNameList.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        self.verticalLayout.addWidget(self.ruleNameList)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget = QWidget(RuleManageDialog)
        self.widget.setObjectName(u"widget")

        self.horizontalLayout.addWidget(self.widget)

        self.deleteButton = QPushButton(RuleManageDialog)
        self.deleteButton.setObjectName(u"deleteButton")

        self.horizontalLayout.addWidget(self.deleteButton)

        self.closeButton = QPushButton(RuleManageDialog)
        self.closeButton.setObjectName(u"closeButton")

        self.horizontalLayout.addWidget(self.closeButton)

        self.horizontalLayout.setStretch(0, 1)

        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(RuleManageDialog)

        QMetaObject.connectSlotsByName(RuleManageDialog)
    # setupUi

    def retranslateUi(self, RuleManageDialog):
        RuleManageDialog.setWindowTitle(QCoreApplication.translate("RuleManageDialog", u"\u89c4\u5219\u7ba1\u7406", None))
        self.deleteButton.setText(QCoreApplication.translate("RuleManageDialog", u"\u5220\u9664", None))
        self.closeButton.setText(QCoreApplication.translate("RuleManageDialog", u"\u5173\u95ed", None))
    # retranslateUi

