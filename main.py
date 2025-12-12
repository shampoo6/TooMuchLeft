import os
import sys
import threading
from queue import Queue
from typing import TypedDict

import pathspec
from PySide6.QtCore import Slot, Qt, QThreadPool, Signal, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog, QMessageBox

from exceptions.delete_exception import DeleteException
from exceptions.message_exception import MessageException, MessageType
from exceptions.search_exception import SearchException
from helpers.delete_runnable import DeleteRunnable
from helpers.rule_manager import RuleManager, SavedData, RuleData
from helpers.search_runnable import SearchRunnable
from helpers.unit_exception_handler import UnitExceptionHandler
from uic.main_table_widget import Ui_MainWindow
from utils import run_as_admin
from widgets.custom_file_size_dialog import CustomFileSizeDialog
from constants import base_dir
from widgets.load_rule_dialog import LoadRuleDialog
from widgets.rule_manage_dialog import RuleManageDialog
from widgets.status_bar import StatusBar


class SearchMeta(TypedDict):
    # 是否在搜索业务中
    # 搜索业务: 包括搜索和建立表格的过程
    searching: bool
    # 搜索文件是否结束，并不带表表格建立的过程结束
    search_done: bool
    # 等待搜索结果的线程
    thread: threading.Thread | None
    # 等待搜索结束的 QTimer，搜索结束后会进行表格加载
    wait_for_search_done_timer: QTimer | None
    # 取消事件
    cancel_event: threading.Event | None


class DeleteMeta(TypedDict):
    # 删除中状态
    deleting: bool
    # 取消事件
    cancel_event: threading.Event | None
    # 进度条用的线程和timer
    progress_thread: threading.Thread | None
    progress_timer: QTimer | None
    # 等待删除文件线程完成的等待线程和timer
    wait_for_delete_done_thread: threading.Thread | None
    wait_for_delete_done_timer: QTimer | None
    # 是否删除完成
    delete_done: bool


class MainWindow(QMainWindow, Ui_MainWindow):
    searching_change = Signal()
    deleting_change = Signal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('删不尽')

        # 初始化全局异常处理器
        self.unit_exception_handler = UnitExceptionHandler.get_instance()
        self.register_exception_handler()

        self.thread_pool = QThreadPool.globalInstance()
        self.custom_file_size_dialog = None
        self.rule_manage_dialog = None
        self.load_rule_dialog = None

        # 搜索相关属性
        self.search_meta: SearchMeta = {
            'searching': False,
            'search_done': False,
            'thread': None,
            'wait_for_search_done_timer': None,
            'cancel_event': None
        }

        # 删除文件的取消事件
        self.delete_meta: DeleteMeta = {
            'deleting': False,
            'cancel_event': None,
            'progress_thread': None,
            'progress_timer': None,
            'wait_for_delete_done_thread': None,
            'wait_for_delete_done_timer': None,
            'delete_done': False
        }

        # 状态栏
        self.status = StatusBar(self)
        self.setStatusBar(self.status)

        # 工具栏
        self.actionSave.triggered.connect(self.on_save)
        self.actionSaveAs.triggered.connect(self.on_save_as)
        self.actionLoad.triggered.connect(self.on_load_rule)
        self.actionQuit.triggered.connect(self.close)

        self.actionSave.setShortcut('Ctrl + S')
        self.actionSaveAs.setShortcut('Ctrl + Shift + S')

        # 规则选择
        RuleManager.get_instance().currentIdChanged.connect(self.update_rule_name_box_and_rule_list)
        self.ruleSpliter.setStretchFactor(0, 2)
        self.ruleSpliter.setStretchFactor(1, 1)
        self.ruleManageButton.clicked.connect(self.on_manage_rules)
        self.ruleNameBox.currentTextChanged.connect(self.on_rule_name_changed)
        self.update_rule_name_box_and_rule_list()

        # 目录选择
        self.selectDirButton.clicked.connect(self.on_select_dir)

        # 文件大小选择
        self.moreSizeButton.clicked.connect(self.on_more_size)

        # 搜索按钮
        self.searchButton.clicked.connect(self.on_search)
        self.searchButton.setShortcut('Ctrl + Return')
        self.searchCancelButton.clicked.connect(self.on_cancel_search)
        self.searchCancelButton.setVisible(False)
        self.searching_change.connect(self.on_searching_change)

        # 文件列表
        self.selectAllButton.clicked.connect(self.fileTable.select_all)
        self.unselectAllButton.clicked.connect(self.fileTable.unselect_all)
        self.deleteButton.clicked.connect(self.on_delete)
        self.deleteButton.setShortcut('Ctrl + D')
        self.deleting_change.connect(self.on_deleting_change)
        self.deleteCancelButton.setVisible(False)
        self.deleteCancelButton.clicked.connect(self.on_cancel_delete)
        self.fileTable.loaded.connect(self.on_file_table_loaded)

        self.status.ready_message()

    def closeEvent(self, e) -> None:
        # 询问是否保存配置
        if self.has_diff_with_saved_data():
            reply = QMessageBox.question(self, '保存', '规则有变化是否保存配置？',
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.on_save()
        if self.search_meta['cancel_event'] is not None and not self.search_meta['cancel_event'].is_set():
            self.search_meta['cancel_event'].set()

    # ========================== 异常处理

    def register_exception_handler(self):
        self.unit_exception_handler.default_handler = self.default_exception_handler
        self.unit_exception_handler.add_handler(MessageException, self.message_exception_handler)
        self.unit_exception_handler.add_handler(SearchException, self.search_exception_handler)
        self.unit_exception_handler.add_handler(DeleteException, self.delete_exception_handler)

    def default_exception_handler(self, exctype, value, traceback_obj):
        QMessageBox.critical(self, '错误', str(value))

    def message_exception_handler(self, exctype, value, traceback_obj):
        title = value.title
        message = value.message
        msg_type = value.msg_type
        if msg_type == MessageType.INFO:
            message_fn = QMessageBox.information
        elif msg_type == MessageType.WARNING:
            message_fn = QMessageBox.warning
        elif msg_type == MessageType.ERROR:
            message_fn = QMessageBox.critical
        else:
            message_fn = QMessageBox.information
        message_fn(self, title, message)

    def search_exception_handler(self, exctype, value, traceback_obj):
        self.set_searching(False)
        QMessageBox.critical(self, '搜索异常', str(value))

    def delete_exception_handler(self, exctype, value, traceback_obj):
        if self.delete_meta['cancel_event'] is not None and not self.delete_meta['cancel_event'].is_set():
            self.delete_meta['cancel_event'].set()
        QMessageBox.critical(self, '删除异常', str(value))

    # ==========================

    def update_rule_name_box(self):
        self.ruleNameBox.blockSignals(True)
        self.ruleNameBox.clear()
        data: SavedData = RuleManager.get_instance().data
        for _id, rule in data['rules'].items():
            self.ruleNameBox.addItem(rule['name'], _id)
        if data['current_id'] is not None:
            self.ruleNameBox.setCurrentText(data['rules'][data['current_id']]['name'])
        self.ruleNameBox.blockSignals(False)

    def update_rule_list(self):
        data: SavedData = RuleManager.get_instance().data
        if data['current_id'] is None:
            return
        current_data = data['rules'][data['current_id']]
        self.includeRuleList.load(current_data['include'])
        self.excludeRuleList.load(current_data['exclude'])

    def get_current_rules(self):
        """获取当前 includeRuleList 和 excludeRuleList 的数据"""
        include_rules = [self.includeRuleList.item(i).text() for i in range(self.includeRuleList.count())]
        exclude_rules = [self.excludeRuleList.item(i).text() for i in range(self.excludeRuleList.count())]
        return include_rules, exclude_rules

    def has_diff_with_saved_data(self):
        include_rules, exclude_rules = self.get_current_rules()
        data: SavedData = RuleManager.get_instance().data
        current_rule = data['rules'][data['current_id']]
        return include_rules != current_rule['include'] or exclude_rules != current_rule['exclude']

    def set_searching(self, searching):
        """设置是否处于搜索中的状态"""
        changed = self.search_meta['searching'] != searching
        self.search_meta['searching'] = searching
        if changed:
            self.searching_change.emit()

    def set_deleting(self, deleting):
        changed = self.delete_meta['deleting'] != deleting
        self.delete_meta['deleting'] = deleting
        if changed:
            self.deleting_change.emit()

    # =================== 槽

    # =================== 工具栏
    @Slot()
    def on_save(self):
        current_id = RuleManager.get_instance().data['current_id']
        if current_id is None:
            self.on_save_as()
        else:
            include_rules, exclude_rules = self.get_current_rules()
            rule_data: RuleData = {
                "name": self.ruleNameBox.currentText(),
                "include": include_rules,
                "exclude": exclude_rules
            }
            _id = self.ruleNameBox.currentData()
            if not RuleManager.get_instance().update_rule(_id, rule_data):
                QMessageBox.critical(self, '保存失败', '找不到对应 _id')

    @Slot()
    def on_save_as(self):
        rule_name, ok = QInputDialog.getText(self, '另存为', '请输入规则名:')
        if not ok:
            return
        include_rules, exclude_rules = self.get_current_rules()
        rule_data: RuleData = {
            "name": rule_name,
            "include": include_rules,
            "exclude": exclude_rules
        }
        if not RuleManager.get_instance().add_rule(rule_data):
            QMessageBox.critical(self, '保存失败', '规则名已存在')
            return
        # 添加规则选项并选中
        if self.ruleNameBox.findText(rule_name) == -1:
            self.ruleNameBox.blockSignals(True)
            self.ruleNameBox.addItem(rule_name, RuleManager.get_instance().data['current_id'])
            self.ruleNameBox.setCurrentText(rule_name)
            self.ruleNameBox.blockSignals(False)

    @Slot()
    def on_load_rule(self):
        self.load_rule_dialog = LoadRuleDialog(self)
        self.load_rule_dialog.open()

    # =================== 规则设置和管理
    @Slot()
    def update_rule_name_box_and_rule_list(self):
        """当前规则发生变化时，更新视图"""
        self.update_rule_name_box()
        self.update_rule_list()

    @Slot()
    def on_rule_name_changed(self, text):
        if isinstance(text, str) and text.strip() != '':
            rule_id = self.ruleNameBox.currentData()
            RuleManager.get_instance().switch_rule(rule_id)

    @Slot()
    def on_select_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, '选择目录',
                                                    base_dir if self.dir_edit.text() == '' else self.dir_edit.text())
        if dir_path != '':
            self.dir_edit.setText(dir_path)

    @Slot()
    def on_more_size(self):
        self.custom_file_size_dialog = CustomFileSizeDialog(self)
        self.custom_file_size_dialog.accepted.connect(self.on_custom_file_size_dialog_confirm)
        self.custom_file_size_dialog.open()

    @Slot()
    def on_custom_file_size_dialog_confirm(self):
        size = self.custom_file_size_dialog.sizeBox.value()
        unit = self.custom_file_size_dialog.unitBox.currentText()
        self.sizeBox.addItem(f"{size}{unit}")
        self.sizeBox.setCurrentText(f"{size}{unit}")

    @Slot()
    def on_manage_rules(self):
        self.rule_manage_dialog = RuleManageDialog()
        self.rule_manage_dialog.open()

    # =================== 搜索

    @Slot()
    def on_searching_change(self):
        self.searchButton.setVisible(not self.search_meta['searching'])
        self.searchCancelButton.setVisible(self.search_meta['searching'])

    @Slot()
    def on_cancel_search(self):
        cancel_event = self.search_meta['cancel_event']
        if cancel_event is not None and not cancel_event.is_set():
            cancel_event.set()

    @Slot()
    def on_search(self):
        dir_path = self.dir_edit.text()
        if dir_path == '':
            QMessageBox.warning(self, '警告', '请选择一个搜索目录')
            return
        if not os.path.exists(dir_path):
            QMessageBox.critical(self, '错误', '目录不存在')
            return

        self.set_searching(True)
        cancel_event = threading.Event()
        self.search_meta['cancel_event'] = cancel_event

        include_rules, exclude_rules = self.get_current_rules()
        include_spec = pathspec.PathSpec.from_lines('gitwildmatch', include_rules) if len(include_rules) > 0 else None
        exclude_spec = pathspec.PathSpec.from_lines('gitwildmatch', exclude_rules) if len(exclude_rules) > 0 else None

        data_queue = Queue()
        rab = SearchRunnable(cancel_event, data_queue, include_spec, exclude_spec, dir_path,
                             self.compareBox.currentText(),
                             self.sizeBox.currentText())
        self.thread_pool.start(rab)

        self.search_meta['search_done'] = False
        self.status.show_emoji_tip('搜索中')

        def wait_for_done():
            self.thread_pool.waitForDone(-1)
            self.search_meta['search_done'] = True
            self.status.show_emoji_tip('渲染搜索结果中')

        self.search_meta['thread'] = threading.Thread(target=wait_for_done, daemon=True)
        self.search_meta['thread'].start()

        @Slot()
        def wait_for_build_table():
            if self.search_meta['search_done']:
                # 构建表格
                table_datas = []
                while not data_queue.empty():
                    table_datas.append(data_queue.get())
                table_datas = sorted(table_datas, key=lambda x: x[2])
                self.fileTable.load_table(cancel_event, table_datas)
                self.search_meta['wait_for_search_done_timer'].stop()

        self.search_meta['wait_for_search_done_timer'] = QTimer(interval=100)
        self.search_meta['wait_for_search_done_timer'].timeout.connect(wait_for_build_table)
        self.search_meta['wait_for_search_done_timer'].start()

    @Slot(bool)
    def on_file_table_loaded(self, success):
        self.set_searching(False)
        msg = '✅搜索完成' if success else '❌取消搜索'
        self.status.set_message(msg, 3000)

    # =================== 删除
    @Slot()
    def on_deleting_change(self):
        self.deleteButton.setVisible(not self.delete_meta['deleting'])
        self.deleteCancelButton.setVisible(self.delete_meta['deleting'])

    @Slot()
    def on_delete(self):
        # 搜集所有勾选项
        delete_datas = self.fileTable.get_checked_path()
        total_step = len(delete_datas)
        if total_step == 0:
            return
        # 增加一步，用于删除 ui 界面中的选项
        total_step += 1

        result = QMessageBox.question(self, '删除', '确定删除吗？',
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                      QMessageBox.StandardButton.No)
        if result == QMessageBox.StandardButton.No:
            return

        self.set_deleting(True)
        self.delete_meta['delete_done'] = False

        show_progress = self.disableProgressCheckBox.checkState() == Qt.CheckState.Unchecked
        if show_progress:
            self.status.start_progress('删除中', 0, total_step)

        queue = Queue() if show_progress else None
        self.delete_meta['cancel_event'] = threading.Event() if show_progress else None
        for abs_path, is_dir in delete_datas:
            rab = DeleteRunnable(abs_path, is_dir, queue, self.delete_meta['cancel_event'])
            self.thread_pool.start(rab)

        current_step = 0
        if show_progress:
            def update_current_step():
                nonlocal current_step
                while current_step < total_step - 1:
                    if self.delete_meta['cancel_event'].is_set():
                        break
                    try:
                        queue.get(timeout=0.1)
                    except:
                        continue
                    current_step += 1

            thread = threading.Thread(target=update_current_step, daemon=True)
            thread.start()
            self.delete_meta['progress_thread'] = thread

            @Slot()
            def update_progress():
                if self.delete_meta['cancel_event'].is_set():
                    self.delete_meta['progress_timer'].stop()
                    return
                self.status.progress.setValue(current_step)
                if current_step >= total_step:
                    self.delete_meta['progress_timer'].stop()

            timer = QTimer(interval=0)
            timer.timeout.connect(update_progress)
            timer.start()
            self.delete_meta['progress_timer'] = timer

        def wait_for_done():
            self.thread_pool.waitForDone(-1)
            self.delete_meta['delete_done'] = True

        thread = threading.Thread(target=wait_for_done, daemon=True)
        thread.start()
        self.delete_meta['wait_for_delete_done_thread'] = thread

        @Slot()
        def after_wait_for_done():
            nonlocal current_step
            if self.delete_meta['delete_done']:
                self.delete_meta['wait_for_delete_done_timer'].stop()
                if show_progress and self.delete_meta['cancel_event'].is_set():
                    self.status.progress.setValue(total_step)
                    QTimer.singleShot(0, lambda: self.status.set_message('❌取消删除', 3000))
                else:
                    if show_progress:
                        current_step += 1
                    self.fileTable.delete_checked()
                    QTimer.singleShot(0, lambda: self.status.set_message('✅删除完成', 3000))
                self.set_deleting(False)

        timer = QTimer(interval=0)
        timer.timeout.connect(after_wait_for_done)
        timer.start()
        self.delete_meta['wait_for_delete_done_timer'] = timer

    @Slot()
    def on_cancel_delete(self):
        cancel_event = self.delete_meta['cancel_event']
        if cancel_event is not None and not cancel_event.is_set():
            cancel_event.set()


# 打包时应使用此代码，让用户授权管理员权限
if not run_as_admin():
    print("用户取消授权或发生错误")
    sys.exit(1)

app = QApplication(sys.argv)
app.setWindowIcon(QIcon(os.path.join(base_dir, 'icon.ico')))

window = MainWindow()
window.show()

app.exec()
