import concurrent.futures
import os

from PySide6.QtCore import QRunnable, QObject, Signal, QThreadPool

from utils import dir_size, file_size_to_byte


class Emitter(QObject):
    reporter = Signal()


class SearchRunnable(QRunnable):
    # data_queue: 存储输出数据的队列
    # compare: 比较方法，小于 或 大于等于，用于比较文件大小，过滤文件
    # compare_size: 比较文件大小时的尺寸 若为 `大小不限` 则不用过滤文件大小
    def __init__(self, data_queue, spec, root, compare, compare_size):
        super().__init__()
        self.data_queue = data_queue
        self.spec = spec
        self.root = root
        self.compare = compare
        self.src_compare_size = compare_size
        self.skip_size_filter = compare_size == '不限大小'
        self.compare_size = file_size_to_byte(compare_size) if not self.skip_size_filter else 0
        self.emitter = Emitter()

    def match(self, pth):
        abs_path = os.path.join(self.root, pth)
        matched = self.spec.match_file(pth)
        is_dir = os.path.isdir(abs_path)
        if matched:
            size = dir_size(abs_path) if is_dir else os.path.getsize(abs_path)
        else:
            size = 0
        return matched, pth, abs_path, is_dir, size

    def size_filter(self, match_tuple):
        operator = '<' if self.compare == '小于' else '>='
        return eval(f'{match_tuple[-1]} {operator} {self.compare_size}')

    def run(self, /) -> None:
        list_dir_result = os.listdir(self.root)
        with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            fs = [executor.submit(self.match, pth) for pth in list_dir_result]
            match_result = [future.result() for future in concurrent.futures.as_completed(fs)]
        # 需要递归的数据: 与 spec 不匹配的目录
        need_recursive = list(filter(lambda match_tuple: not match_tuple[0] and match_tuple[-2], match_result))
        match_result = [result[1:] for result in match_result if result[0]]
        if not self.skip_size_filter:
            match_result = list(filter(self.size_filter, match_result))
        for pth, abs_path, is_dir, size in match_result:
            ext_name = os.path.splitext(abs_path)[-1].lower()
            self.data_queue.put((self.root, pth, abs_path, is_dir, ext_name, size))
        if len(need_recursive) > 0:
            for match_tuple in need_recursive:
                rab = SearchRunnable(self.data_queue, self.spec, match_tuple[2], self.compare, self.src_compare_size)
                QThreadPool.globalInstance().start(rab)
