import queue
import sys
import threading

from PySide6.QtCore import QObject, QTimer


class UnitExceptionHandler(QObject):
    """
    全局异常处理器
    该类必须在主线程中创建实例
    异常处理程序会在主线程中执行
    """

    instance = None

    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()
        self.error_queue = queue.Queue()

        # key: 异常类型
        # value: 处理函数，处理函数会收到三个参数 exctype, value, traceback_obj 分别代表:
        # exctype: 异常类型
        # value: 异常实例
        # traceback_obj: traceback 对象
        self.handler_map: dict[type(Exception), callable] = {}
        sys.excepthook = self._handle_error

        # 默认处理器
        self.default_handler = None

        self.read_queue_timer = QTimer(interval=0)
        self.read_queue_timer.timeout.connect(self._read_queue)
        self.read_queue_timer.start()

    @staticmethod
    def get_instance():
        if UnitExceptionHandler.instance is None:
            UnitExceptionHandler.instance = UnitExceptionHandler()
        return UnitExceptionHandler.instance

    def _handle_error(self, exctype, value, traceback_obj):
        self.error_queue.put((exctype, value, traceback_obj))

    def _read_queue(self):
        try:
            exp_tuple = self.error_queue.get_nowait()
            exctype, value, traceback_obj = exp_tuple
            if exctype in self.handler_map:
                self.handler_map[exctype](exctype, value, traceback_obj)
            elif self.default_handler is not None:
                self.default_handler(exctype, value, traceback_obj)
        except:
            pass

    def add_handler(self, exctype, handler):
        self.handler_map[exctype] = handler

    def delete_handler(self, exctype):
        if exctype in self.handler_map:
            del self.handler_map[exctype]
