import concurrent.futures
import os
import stat
from enum import Enum

from PySide6.QtCore import QRunnable, QThreadPool

from exceptions.search_exception import SearchException
from utils import dir_size, file_size_to_byte


class MatchType(Enum):
    MATCHED = 0  # 匹配
    NOT_MATCHED = 1  # 不匹配
    EXCLUDED = 2  # 被排除
    PERMISSION_DENIED = 3  # 权限不足


class SearchRunnable(QRunnable):
    # data_queue: 存储输出数据的队列
    # compare: 比较方法，小于 或 大于等于，用于比较文件大小，过滤文件
    # compare_size: 比较文件大小时的尺寸 若为 `大小不限` 则不用过滤文件大小
    def __init__(self, cancel_evnet, data_queue, include_spec, exclude_spec, root, compare, compare_size):
        super().__init__()
        self.cancel_event = cancel_evnet
        self.data_queue = data_queue
        self.include_spec = include_spec
        self.exclude_spec = exclude_spec
        self.root = root
        self.compare = compare
        self.src_compare_size = compare_size
        self.skip_size_filter = compare_size == '不限大小'
        self.compare_size = file_size_to_byte(compare_size) if not self.skip_size_filter else 0

    def match(self, pth):
        abs_path = os.path.join(self.root, pth)
        try:
            st = os.lstat(abs_path)
            if bool(st.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT):
                # 若为特殊重解析点的话，就返回没有权限
                # 重解析点: 文件系统中添加元数据和特殊行为的路径点，例如快捷方式等
                matched = MatchType.PERMISSION_DENIED
            elif self.exclude_spec is not None and self.exclude_spec.match_file(pth):
                matched = MatchType.EXCLUDED
            elif self.include_spec is not None:
                matched = MatchType.MATCHED if self.include_spec.match_file(pth) else MatchType.NOT_MATCHED
            else:
                matched = MatchType.MATCHED
            is_dir = os.path.isdir(abs_path)
            if matched == MatchType.MATCHED:
                size = dir_size(abs_path) if is_dir else os.path.getsize(abs_path)
            else:
                size = 0
            return matched, pth, abs_path, is_dir, size
        except:
            raise SearchException(f'路径: {abs_path} \n搜索该路径时出现异常，这种情况通常是因为该文件或目录被系统保护了\n建议添加名称到排除列表')

    def size_filter(self, match_tuple):
        operator = '<' if self.compare == '小于' else '>='
        return eval(f'{match_tuple[-1]} {operator} {self.compare_size}')

    def run(self, /) -> None:
        if self.cancel_event.is_set():
            return
        list_dir_result = os.listdir(self.root)
        with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            fs = [executor.submit(self.match, pth) for pth in list_dir_result]
            match_result = [future.result() for future in concurrent.futures.as_completed(fs)]
        # 需要递归的数据: 与 spec 不匹配的目录
        need_recursive = list(
            filter(lambda match_tuple: match_tuple[0] == MatchType.NOT_MATCHED and match_tuple[-2], match_result))
        match_result = [result[1:] for result in match_result if result[0] == MatchType.MATCHED]
        if not self.skip_size_filter:
            match_result = list(filter(self.size_filter, match_result))
        for pth, abs_path, is_dir, size in match_result:
            ext_name = os.path.splitext(abs_path)[-1].lower()
            if self.cancel_event.is_set():
                return
            self.data_queue.put((self.root, pth, abs_path, is_dir, ext_name, size))
        if len(need_recursive) > 0:
            runnables = [
                SearchRunnable(self.cancel_event, self.data_queue, self.include_spec, self.exclude_spec, match_tuple[2],
                               self.compare, self.src_compare_size) for match_tuple in need_recursive]
            pool = QThreadPool.globalInstance()
            with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                executor.map(pool.start, runnables)
