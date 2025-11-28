# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QFormLayout, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QListWidgetItem, QMainWindow, QPushButton,
    QSizePolicy, QSplitter, QStatusBar, QToolBar,
    QToolButton, QTreeWidgetItem, QVBoxLayout, QWidget)

from widgets.editable_list import EditableList
from widgets.file_tree import FileTree
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(689, 538)
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        icon = QIcon()
        icon.addFile(u":/icons/save.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionSave.setIcon(icon)
        self.actionSave.setMenuRole(QAction.MenuRole.NoRole)
        self.actionLoad = QAction(MainWindow)
        self.actionLoad.setObjectName(u"actionLoad")
        icon1 = QIcon()
        icon1.addFile(u":/icons/load.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionLoad.setIcon(icon1)
        self.actionLoad.setMenuRole(QAction.MenuRole.NoRole)
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        icon2 = QIcon()
        icon2.addFile(u":/icons/quit.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionQuit.setIcon(icon2)
        self.actionQuit.setMenuRole(QAction.MenuRole.NoRole)
        self.actionAdd = QAction(MainWindow)
        self.actionAdd.setObjectName(u"actionAdd")
        icon3 = QIcon()
        icon3.addFile(u":/icons/add.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionAdd.setIcon(icon3)
        self.actionAdd.setMenuRole(QAction.MenuRole.NoRole)
        self.actionDelete = QAction(MainWindow)
        self.actionDelete.setObjectName(u"actionDelete")
        icon4 = QIcon()
        icon4.addFile(u":/icons/sub.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionDelete.setIcon(icon4)
        self.actionDelete.setMenuRole(QAction.MenuRole.NoRole)
        self.actionSaveAs = QAction(MainWindow)
        self.actionSaveAs.setObjectName(u"actionSaveAs")
        icon5 = QIcon()
        icon5.addFile(u":/icons/save_as.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionSaveAs.setIcon(icon5)
        self.actionSaveAs.setMenuRole(QAction.MenuRole.NoRole)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.splitter.setOpaqueResize(True)
        self.splitter.setHandleWidth(5)
        self.splitter.setChildrenCollapsible(False)
        self.fileContainer = QWidget(self.splitter)
        self.fileContainer.setObjectName(u"fileContainer")
        self.fileContainer.setMinimumSize(QSize(400, 0))
        self.fileContainer.setAutoFillBackground(True)
        self.verticalLayout = QVBoxLayout(self.fileContainer)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.fileTree = FileTree(self.fileContainer)
        self.fileTree.setObjectName(u"fileTree")

        self.verticalLayout.addWidget(self.fileTree)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.selectAllButton = QPushButton(self.fileContainer)
        self.selectAllButton.setObjectName(u"selectAllButton")

        self.horizontalLayout_2.addWidget(self.selectAllButton)

        self.unselectAllButton = QPushButton(self.fileContainer)
        self.unselectAllButton.setObjectName(u"unselectAllButton")

        self.horizontalLayout_2.addWidget(self.unselectAllButton)

        self.widget = QWidget(self.fileContainer)
        self.widget.setObjectName(u"widget")

        self.horizontalLayout_2.addWidget(self.widget)

        self.deleteButton = QPushButton(self.fileContainer)
        self.deleteButton.setObjectName(u"deleteButton")

        self.horizontalLayout_2.addWidget(self.deleteButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.splitter.addWidget(self.fileContainer)
        self.ruleContainer = QWidget(self.splitter)
        self.ruleContainer.setObjectName(u"ruleContainer")
        self.ruleContainer.setMinimumSize(QSize(200, 500))
        self.ruleContainer.setAutoFillBackground(True)
        self.formLayout = QFormLayout(self.ruleContainer)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.ruleContainer)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.ruleNameBox = QComboBox(self.ruleContainer)
        self.ruleNameBox.setObjectName(u"ruleNameBox")

        self.horizontalLayout_6.addWidget(self.ruleNameBox)

        self.ruleManageButton = QToolButton(self.ruleContainer)
        self.ruleManageButton.setObjectName(u"ruleManageButton")

        self.horizontalLayout_6.addWidget(self.ruleManageButton)


        self.formLayout.setLayout(0, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_6)

        self.label_4 = QLabel(self.ruleContainer)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_4)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.dir_edit = QLineEdit(self.ruleContainer)
        self.dir_edit.setObjectName(u"dir_edit")
        self.dir_edit.setReadOnly(True)

        self.horizontalLayout_4.addWidget(self.dir_edit)

        self.selectDirButton = QToolButton(self.ruleContainer)
        self.selectDirButton.setObjectName(u"selectDirButton")

        self.horizontalLayout_4.addWidget(self.selectDirButton)


        self.formLayout.setLayout(1, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_4)

        self.label = QLabel(self.ruleContainer)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.sizeBox = QComboBox(self.ruleContainer)
        self.sizeBox.addItem("")
        self.sizeBox.addItem("")
        self.sizeBox.addItem("")
        self.sizeBox.addItem("")
        self.sizeBox.addItem("")
        self.sizeBox.addItem("")
        self.sizeBox.setObjectName(u"sizeBox")

        self.horizontalLayout_3.addWidget(self.sizeBox)

        self.moreSizeButton = QToolButton(self.ruleContainer)
        self.moreSizeButton.setObjectName(u"moreSizeButton")

        self.horizontalLayout_3.addWidget(self.moreSizeButton)


        self.formLayout.setLayout(2, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_3)

        self.label_2 = QLabel(self.ruleContainer)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.compareBox = QComboBox(self.ruleContainer)
        self.compareBox.addItem("")
        self.compareBox.addItem("")
        self.compareBox.setObjectName(u"compareBox")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.compareBox)

        self.label_3 = QLabel(self.ruleContainer)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setCursor(QCursor(Qt.CursorShape.WhatsThisCursor))

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.ruleList = EditableList(self.ruleContainer)
        self.ruleList.setObjectName(u"ruleList")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.ruleList.sizePolicy().hasHeightForWidth())
        self.ruleList.setSizePolicy(sizePolicy)
        self.ruleList.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.ruleList)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.searchButton = QPushButton(self.ruleContainer)
        self.searchButton.setObjectName(u"searchButton")

        self.horizontalLayout_5.addWidget(self.searchButton)


        self.formLayout.setLayout(6, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_5)

        self.disableProgressCheckBox = QCheckBox(self.ruleContainer)
        self.disableProgressCheckBox.setObjectName(u"disableProgressCheckBox")
        self.disableProgressCheckBox.setChecked(True)
        self.disableProgressCheckBox.setTristate(False)

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.disableProgressCheckBox)

        self.splitter.addWidget(self.ruleContainer)

        self.horizontalLayout.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.ToolBarArea.RightToolBarArea, self.toolBar)

        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionSaveAs)
        self.toolBar.addAction(self.actionLoad)
        self.toolBar.addAction(self.actionAdd)
        self.toolBar.addAction(self.actionDelete)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionQuit)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(tooltip)
        self.actionSave.setToolTip(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u89c4\u5219(Ctrl+S)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.actionSave.setStatusTip(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u89c4\u5219(Ctrl+S)", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionLoad.setText(QCoreApplication.translate("MainWindow", u"Load", None))
#if QT_CONFIG(tooltip)
        self.actionLoad.setToolTip(QCoreApplication.translate("MainWindow", u"\u52a0\u8f7d\u89c4\u5219(Ctrl+L)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.actionLoad.setStatusTip(QCoreApplication.translate("MainWindow", u"\u52a0\u8f7d\u4efb\u610f\u6587\u672c\u6587\u4ef6\u4f5c\u4e3a\u89c4\u5219(Ctrl+L)", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(shortcut)
        self.actionLoad.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+L", None))
#endif // QT_CONFIG(shortcut)
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
#if QT_CONFIG(tooltip)
        self.actionQuit.setToolTip(QCoreApplication.translate("MainWindow", u"\u9000\u51fa(Alt+F4)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.actionQuit.setStatusTip(QCoreApplication.translate("MainWindow", u"\u9000\u51fa(Alt+F4)", None))
#endif // QT_CONFIG(statustip)
        self.actionAdd.setText(QCoreApplication.translate("MainWindow", u"Add", None))
#if QT_CONFIG(tooltip)
        self.actionAdd.setToolTip(QCoreApplication.translate("MainWindow", u"\u6dfb\u52a0\u89c4\u5219", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.actionAdd.setStatusTip(QCoreApplication.translate("MainWindow", u"\u6dfb\u52a0\u89c4\u5219", None))
#endif // QT_CONFIG(statustip)
        self.actionDelete.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
#if QT_CONFIG(tooltip)
        self.actionDelete.setToolTip(QCoreApplication.translate("MainWindow", u"\u5220\u9664\u89c4\u5219(Del)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.actionDelete.setStatusTip(QCoreApplication.translate("MainWindow", u"\u5220\u9664\u89c4\u5219(Del)", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(shortcut)
        self.actionDelete.setShortcut(QCoreApplication.translate("MainWindow", u"Del", None))
#endif // QT_CONFIG(shortcut)
        self.actionSaveAs.setText(QCoreApplication.translate("MainWindow", u"SaveAs", None))
#if QT_CONFIG(tooltip)
        self.actionSaveAs.setToolTip(QCoreApplication.translate("MainWindow", u"\u53e6\u5b58\u4e3a(Ctrl+Shift+S)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.actionSaveAs.setStatusTip(QCoreApplication.translate("MainWindow", u"\u53e6\u5b58\u4e3a(Ctrl+Shift+S)", None))
#endif // QT_CONFIG(statustip)
        ___qtreewidgetitem = self.fileTree.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("MainWindow", u"\u6587\u4ef6\u5927\u5c0f", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"\u7c7b\u578b", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"\u6587\u4ef6\u6216\u76ee\u5f55", None));
#if QT_CONFIG(statustip)
        self.selectAllButton.setStatusTip(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u5168\u90e8\u6587\u4ef6\u548c\u76ee\u5f55", None))
#endif // QT_CONFIG(statustip)
        self.selectAllButton.setText(QCoreApplication.translate("MainWindow", u"\u5168\u9009", None))
#if QT_CONFIG(statustip)
        self.unselectAllButton.setStatusTip(QCoreApplication.translate("MainWindow", u"\u53d6\u6d88\u5168\u90e8\u9009\u62e9", None))
#endif // QT_CONFIG(statustip)
        self.unselectAllButton.setText(QCoreApplication.translate("MainWindow", u"\u5168\u4e0d\u9009", None))
#if QT_CONFIG(tooltip)
        self.deleteButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u5220\u9664\u52fe\u9009\u7684\u6587\u4ef6\u548c\u76ee\u5f55(Ctrl+D)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.deleteButton.setStatusTip(QCoreApplication.translate("MainWindow", u"\u5220\u9664\u52fe\u9009\u7684\u6587\u4ef6\u548c\u76ee\u5f55(Ctrl+D)", None))
#endif // QT_CONFIG(statustip)
        self.deleteButton.setText(QCoreApplication.translate("MainWindow", u"\u5220\u9664", None))
#if QT_CONFIG(tooltip)
        self.label_5.setToolTip(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u8bbe\u7f6e\u597d\u7684\u89c4\u5219", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_5.setStatusTip(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u8bbe\u7f6e\u597d\u7684\u89c4\u5219", None))
#endif // QT_CONFIG(statustip)
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u89c4\u5219", None))
#if QT_CONFIG(tooltip)
        self.ruleManageButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u89c4\u5219\u7ba1\u7406", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.ruleManageButton.setStatusTip(QCoreApplication.translate("MainWindow", u"\u89c4\u5219\u7ba1\u7406", None))
#endif // QT_CONFIG(statustip)
        self.ruleManageButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
#if QT_CONFIG(tooltip)
        self.label_4.setToolTip(QCoreApplication.translate("MainWindow", u"\u76ee\u6807\u76ee\u5f55", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_4.setStatusTip(QCoreApplication.translate("MainWindow", u"\u76ee\u6807\u76ee\u5f55", None))
#endif // QT_CONFIG(statustip)
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u76ee\u5f55", None))
        self.dir_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u9009\u62e9\u641c\u7d22\u76ee\u5f55", None))
#if QT_CONFIG(tooltip)
        self.selectDirButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u76ee\u5f55", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.selectDirButton.setStatusTip(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u76ee\u5f55", None))
#endif // QT_CONFIG(statustip)
        self.selectDirButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
#if QT_CONFIG(tooltip)
        self.label.setToolTip(QCoreApplication.translate("MainWindow", u"\u6309\u6587\u4ef6\u5927\u5c0f\u8fc7\u6ee4", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label.setStatusTip(QCoreApplication.translate("MainWindow", u"\u6309\u6587\u4ef6\u5927\u5c0f\u8fc7\u6ee4", None))
#endif // QT_CONFIG(statustip)
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u5927\u5c0f", None))
        self.sizeBox.setItemText(0, QCoreApplication.translate("MainWindow", u"\u4e0d\u9650\u5927\u5c0f", None))
        self.sizeBox.setItemText(1, QCoreApplication.translate("MainWindow", u"10MB", None))
        self.sizeBox.setItemText(2, QCoreApplication.translate("MainWindow", u"100MB", None))
        self.sizeBox.setItemText(3, QCoreApplication.translate("MainWindow", u"500MB", None))
        self.sizeBox.setItemText(4, QCoreApplication.translate("MainWindow", u"1GB", None))
        self.sizeBox.setItemText(5, QCoreApplication.translate("MainWindow", u"5GB", None))

#if QT_CONFIG(tooltip)
        self.moreSizeButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u81ea\u5b9a\u4e49\u5927\u5c0f", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.moreSizeButton.setStatusTip(QCoreApplication.translate("MainWindow", u"\u81ea\u5b9a\u4e49\u5927\u5c0f", None))
#endif // QT_CONFIG(statustip)
        self.moreSizeButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
#if QT_CONFIG(tooltip)
        self.label_2.setToolTip(QCoreApplication.translate("MainWindow", u"\u8fc7\u6ee4\u5c0f\u4e8e\u6216\u5927\u4e8e\u7b49\u4e8e\u6307\u5b9a\u5927\u5c0f\u7684\u6587\u4ef6", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_2.setStatusTip(QCoreApplication.translate("MainWindow", u"\u8fc7\u6ee4\u5c0f\u4e8e\u6216\u5927\u4e8e\u7b49\u4e8e\u6307\u5b9a\u5927\u5c0f\u7684\u6587\u4ef6", None))
#endif // QT_CONFIG(statustip)
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u6bd4\u8f83", None))
        self.compareBox.setItemText(0, QCoreApplication.translate("MainWindow", u"\u5927\u4e8e\u7b49\u4e8e", None))
        self.compareBox.setItemText(1, QCoreApplication.translate("MainWindow", u"\u5c0f\u4e8e", None))

#if QT_CONFIG(tooltip)
        self.label_3.setToolTip(QCoreApplication.translate("MainWindow", u"\u641c\u7d22\u6587\u4ef6\u7684\u89c4\u5219\n"
"\u5177\u4f53\u89c4\u5219\u548c.gitignore\u76f8\u540c", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_3.setStatusTip(QCoreApplication.translate("MainWindow", u"\u641c\u7d22\u6587\u4ef6\u7684\u89c4\u5219\uff0c\u5177\u4f53\u89c4\u5219\u548c.gitignore\u76f8\u540c", None))
#endif // QT_CONFIG(statustip)
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u5177\u4f53\n"
"\u89c4\u5219", None))
#if QT_CONFIG(tooltip)
        self.searchButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u641c\u7d22\u7b26\u5408\u89c4\u5219\u548c\u6587\u4ef6\u5927\u5c0f\u7684\u6587\u4ef6(Ctrl+Enter)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.searchButton.setStatusTip(QCoreApplication.translate("MainWindow", u"\u641c\u7d22\u7b26\u5408\u89c4\u5219\u548c\u6587\u4ef6\u5927\u5c0f\u7684\u6587\u4ef6(Ctrl+Enter)", None))
#endif // QT_CONFIG(statustip)
        self.searchButton.setText(QCoreApplication.translate("MainWindow", u"\u641c\u7d22", None))
#if QT_CONFIG(tooltip)
        self.disableProgressCheckBox.setToolTip(QCoreApplication.translate("MainWindow", u"\u7981\u7528\u8fdb\u5ea6\u6761\u5220\u9664\u6587\u4ef6\u4f1a\u66f4\u5feb", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.disableProgressCheckBox.setStatusTip(QCoreApplication.translate("MainWindow", u"\u7981\u7528\u8fdb\u5ea6\u6761\u5220\u9664\u6587\u4ef6\u4f1a\u66f4\u5feb", None))
#endif // QT_CONFIG(statustip)
        self.disableProgressCheckBox.setText(QCoreApplication.translate("MainWindow", u"\u7981\u7528\u8fdb\u5ea6\u6761", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

