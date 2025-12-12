import json
import os.path
import uuid
from typing import TypedDict

from PySide6.QtCore import QObject, Signal

from constants import base_dir


class RuleData(TypedDict):
    """一条规则数据"""
    # 规则名称
    name: str
    # 包含规则
    include: list[str]
    # 排除规则
    exclude: list[str]


class SavedData(TypedDict):
    """保存的数据"""
    # 当前使用的规则 id
    current_id: str | None
    # 规则字典
    # key: uuidv4
    # value: 一条规则数据
    rules: dict[str, RuleData]


class RuleManager(QObject):
    # 当前 id 变化信号
    currentIdChanged = Signal()

    instance = None

    def __init__(self):
        super().__init__()
        self.save_path = os.path.join(base_dir, 'rules.json')
        if os.path.exists(self.save_path):
            with open(self.save_path, 'r', encoding='utf-8') as f:
                self.data: SavedData = json.load(f)
                if self.data['current_id'] is not None:
                    self.currentIdChanged.emit()
        else:
            self.data: SavedData = {
                'current_id': None,
                'rules': {}
            }

    @staticmethod
    def get_instance():
        if RuleManager.instance is None:
            RuleManager.instance = RuleManager()
        return RuleManager.instance

    def sync_data(self):
        """同步数据到保存的文件中"""
        with open(self.save_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def switch_rule(self, _id: str):
        """
        切换规则
        :param _id: 规则id
        :return: 是否切换成功
        """
        if _id not in self.data['rules']:
            return False
        self.data['current_id'] = _id
        self.sync_data()
        self.currentIdChanged.emit()
        return True

    def add_rule(self, data: RuleData):
        """
        添加规则
        :param data: 规则数据
        :return: 是否添加成功
        """
        # 判断是否同名
        if any([data['name'] == rule_data['name'] for rule_data in self.data['rules'].values()]):
            return False
        _id = str(uuid.uuid4())
        self.data['rules'][_id] = data
        # 将当前 id 设置为 _id
        self.data['current_id'] = _id
        self.sync_data()
        self.currentIdChanged.emit()
        return True

    def delete_rule(self, _id_or_id_list: str | list[str]):
        """
        删除规则
        :param _id_or_id_list: 要删除的 id 或 id 列表
        :return: 是否删除成功
        """
        if isinstance(_id_or_id_list, str):
            _ids = [_id_or_id_list]
        else:
            _ids = _id_or_id_list
        for _id in _ids:
            if _id not in self.data['rules']:
                return False
            del self.data['rules'][_id]
            if self.data['current_id'] == _id:
                self.data['current_id'] = None if len(self.data['rules']) == 0 else list(self.data['rules'].keys())[0]
        self.sync_data()
        self.currentIdChanged.emit()
        return True

    def update_rule(self, _id, data: RuleData):
        """
        更新规则
        :param _id: 规则 id
        :param data: 规则数据
        :return: 是否更新成功
        """
        if _id not in self.data['rules']:
            return False
        self.data['rules'][_id] = data
        self.sync_data()
        return True
