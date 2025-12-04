import os
import shutil
import stat

from PySide6.QtCore import QRunnable


class DeleteRunnable(QRunnable):
    def __init__(self, pth, is_dir, queue=None, cancel_event=None):
        super().__init__()
        self.queue = queue
        self.cancel_event = cancel_event
        self.pth = pth
        self.is_dir = is_dir

    def _on_error(self, func, pth, _):
        if os.path.isfile(pth):
            self.delete_file(pth)

    def delete_file(self, pth):
        os.chmod(pth, stat.S_IWRITE)
        os.remove(pth)

    def run(self):
        if self.cancel_event is not None and self.cancel_event.is_set():
            return
        if self.is_dir:
            shutil.rmtree(self.pth, onerror=self._on_error)
        else:
            self.delete_file(self.pth)
        if self.queue is not None:
            self.queue.put(self.pth)
