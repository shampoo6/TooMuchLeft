import ctypes
import os.path
import re
import sys

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


# 获取目录大小
def dir_size(dir_path):
    current_size = 0
    for entry in os.scandir(dir_path):
        if entry.is_file():
            current_size += os.path.getsize(entry.path)
        else:
            current_size += dir_size(entry.path)
    return current_size


def run_as_admin():
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True  # 已经是管理员

    # 使用 pythonw.exe（无控制台）
    pythonw = sys.executable.replace("python.exe", "pythonw.exe")

    # 重新启动自身，并请求管理员权限
    params = " ".join([f'"{arg}"' for arg in sys.argv])

    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", pythonw, params, None, 1
        )
    except Exception as e:
        return False

    sys.exit(0)  # 退出当前非管理员进程
