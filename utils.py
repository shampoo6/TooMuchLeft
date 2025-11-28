import os.path
import re

units = ['B', 'KB', 'MB', 'GB', 'TB']

regex = re.compile(r'(\d+)(B|KB|MB|GB|TB)')


def file_size_to_byte(size_str):
    match = regex.search(size_str)
    if match is None:
        raise Exception(f'无效的文件大小字符串: {size_str}')
    num, unit = match.groups()
    size = int(num) * pow(1024, units.index(unit))
    return size


def byte_size_to_str(byte_size):
    current_unit_idx = 0
    while byte_size >= 1024 and current_unit_idx < len(units) - 1:
        byte_size /= 1024
        current_unit_idx += 1
    return f'{byte_size:.2f}{units[current_unit_idx]}'


def file_meta(file_path):
    file_path = os.path.normpath(file_path)
    ext_split = os.path.splitext(file_path)
    ext_name = ext_split[-1].upper()
    file_size = os.path.getsize(file_path)
    return ext_name, file_size


# 分析路径
def path_analysis(file_path):
    file_path = os.path.normpath(file_path)
    splits = file_path.split(os.sep)
    return splits
