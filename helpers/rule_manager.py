import json
import os.path
from typing import TypedDict

from constants import base_dir


class RuleManager:
    class RuleData(TypedDict):
        # current: 当前规则
        current: str | None
        # rules: 规则对象
        #   key: 规则名称
        #   value: 规则字符串列表
        rules: dict[str, list[str]]

    instance = None

    def __init__(self):
        self.save_path = os.path.join(base_dir, 'rules.json')
        # rule_data keys:
        # current: 当前规则
        # rules: 规则对象
        #   key: 规则名称
        #   value: 规则字符串列表
        self.rule_data: RuleManager.RuleData = {'current': None, 'rules': {}}
        if os.path.exists(self.save_path):
            with open(self.save_path, 'r', encoding='utf-8') as f:
                self.rule_data = json.load(f)

    @staticmethod
    def get_instance():
        if RuleManager.instance is None:
            RuleManager.instance = RuleManager()
        return RuleManager.instance

    def update(self):
        with open(self.save_path, 'w', encoding='utf-8') as f:
            json.dump(self.rule_data, f, ensure_ascii=False, indent=4)

    def save(self, rule_name, rules):
        """
        保存规则
        :param rule_name: 规则名
        :param rules: 规则文本列表
        :return:
        """
        if self.rule_data['current'] != rule_name:
            self.rule_data['current'] = rule_name

        self.rule_data['rules'][rule_name] = rules
        self.update()

    def setCurrent(self, current):
        if isinstance(current, str) and current.strip() != '' and current != self.rule_data['current']:
            self.rule_data['current'] = current
            self.update()
