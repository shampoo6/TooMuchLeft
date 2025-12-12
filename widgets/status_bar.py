import random

from PySide6.QtCore import Slot, Signal, QTimer
from PySide6.QtWidgets import QStatusBar, QLabel, QProgressBar, QSizePolicy


class StatusBar(QStatusBar):
    _ready_text = '欢迎使用 删不尽！'
    _emojis = '😀😁😂🤣😃😄😅😆😉😊😋😎😍😘🥰😗😙😚🙂🤗🤩🤔🤨😐😑😶🙄😏😣😥😮🤐😯😪😫🥱😴😌😛😜😝🤤😒😓😔😕🙃🤑😲🙁😖😞😟😤😢😭😦😧😨😩🤯😬😰😱🥵🥶😳🤪😵🥴😠😡🤬😷🤒🤕🤢🤮🤧😇🥳🥺🤠🤡🤥🤫🤭🧐🤓😈👿👹👺💀'

    def __init__(self, parent=None):
        super().__init__(parent)
        # 常驻消息
        self.message = QLabel()

        # 常驻进度条
        self.progress = QProgressBar()
        self.progress.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.progress.setStyleSheet("""
/* 整体样式 */
QProgressBar {
    height: 20px;
    text-align: center;
}
/* 已完成部分 */
QProgressBar::chunk {
}
""")
        self.progress.valueChanged.connect(self.on_value_changed)
        self.progress.hide()

        self.addPermanentWidget(self.progress)
        self.addPermanentWidget(self.message)

        # 进度条用的 emoji
        self.progress_emoji_count = 3
        self._emoji_idx = self._random_emoji(self.progress_emoji_count)
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self._update_progress_tip)
        self.progress_msg = ''

    def _random_emoji(self, count):
        return [random.randint(0, len(self._emojis) - 1) for _ in range(count)]

    def _update_progress_tip(self):
        i, = self._random_emoji(1)
        self._emoji_idx.pop(-1)
        self._emoji_idx.insert(0, i)
        self.show_emoji_tip(self.progress_msg, emoji_idx=self._emoji_idx)

    @Slot()
    def on_value_changed(self):
        if self.progress.value() >= self.progress.maximum():
            self.progress_timer.stop()
            self.progress.hide()

    def set_message(self, msg: str, duration=0):
        """
        显示消息
        :param msg: 消息
        :param duration: 显示时常，0 代表常驻
        :return:
        """
        self.message.setText(msg)
        if duration != 0:
            QTimer.singleShot(duration, self.ready_message)

    def ready_message(self):
        self.show_emoji_tip(self._ready_text, 3)

    def start_progress(self, msg, _min, _max, interval=1000):
        self.progress.setRange(_min, _max)
        self.progress.setValue(0)
        self.progress.show()

        self.progress_msg = msg
        self.show_emoji_tip(msg, emoji_idx=self._emoji_idx)
        self.progress_timer.start(interval)

    def show_emoji_tip(self, msg: str, emoji_count=3, emoji_idx=None):
        emoji_idx = emoji_idx or self._random_emoji(emoji_count)
        text = f'{msg}{"".join([self._emojis[i] for i in emoji_idx])}'
        self.set_message(text)
