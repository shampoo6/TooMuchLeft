import os
import shutil
import stat

from PySide6.QtCore import QRunnable

from exceptions.delete_exception import DeleteException


def _delete_file(pth):
    try:
        os.chmod(pth, stat.S_IWRITE)
        os.remove(pth)
    except Exception as e:
        raise DeleteException(str(e), pth)


def _on_error(func, pth, _):
    if os.path.isfile(pth):
        _delete_file(pth)
    else:
        raise DeleteException(f'目录删除失败: {pth}', pth)


class DeleteRunnable(QRunnable):
    def __init__(self, pth, is_dir, queue=None, cancel_event=None):
        super().__init__()
        self.queue = queue
        self.cancel_event = cancel_event
        self.pth = pth
        self.is_dir = is_dir

    def run(self):
        if self.cancel_event is not None and self.cancel_event.is_set():
            return
        if self.is_dir:
            shutil.rmtree(self.pth, onerror=_on_error)
        else:
            _delete_file(self.pth)
        if self.queue is not None:
            self.queue.put(self.pth)
