import concurrent.futures
import os.path
import re

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTreeWidgetItem

from constants import PathType

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
    splits = list(filter(lambda pth: pth.strip() != '', splits))
    return splits


# 获取目录大小
def dir_size(dir_path):
    current_size = 0
    for entry in os.scandir(dir_path):
        if entry.is_file():
            current_size += os.path.getsize(entry.path)
        else:
            current_size += dir_size(entry.path)
    return current_size


def _spec_match_file(spec, pth):
    return spec.match_file(pth), pth


def _match_fs_tree_layer(spec, paths, layers):
    # 当前层的索引就是深度
    # current_layers 中包含的元组数据分别是 (file_path, is_dir, file_size)
    current_layers = []
    next_layer_paths = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() * 2) as executor:
        fs = [executor.submit(_spec_match_file, spec, pth) for pth in paths]
        match_result = [future.result() for future in concurrent.futures.as_completed(fs)]
    for match, pth in match_result:
        is_dir = os.path.isdir(pth)
        if match:
            size = dir_size(pth) if is_dir else os.path.getsize(pth)
            current_layers.append((pth, is_dir, size))
        elif is_dir:
            next_layer_paths += [os.path.normpath(os.path.join(pth, child)) for child in os.listdir(pth)]
    if len(current_layers) > 0:
        current_layers = sorted(current_layers, key=lambda x: x[0])
        layers.append(current_layers)
    if len(next_layer_paths) > 0:
        return _match_fs_tree_layer(spec, next_layer_paths, layers)
    else:
        return layers


# 使用规则匹配路径
def match_files(spec, dir_path):
    dir_list = os.listdir(dir_path)
    if len(dir_list) == 0:
        return None
    return _match_fs_tree_layer(spec, [os.path.normpath(os.path.join(dir_path, pth)) for pth in dir_list], [])


def create_tree_item(pth, abs_path, is_dir, ext_name, size):
    item = QTreeWidgetItem()
    item.setText(0, pth)
    item.setText(1, ext_name)
    item.setText(2, byte_size_to_str(size) if size != '' else '')
    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
    item.setCheckState(0, Qt.CheckState.Checked)
    item.setToolTip(0, os.path.normpath(abs_path))
    item.setData(0, Qt.ItemDataRole.UserRole, PathType.DIR if is_dir else PathType.FILE)
    return item
