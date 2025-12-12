class MessageType:
    INFO = 0  # 信息
    WARNING = 1  # 警告
    ERROR = 2  # 错误


class MessageException(Exception):
    """希望显示消息对话框的异常"""

    def __init__(self, title: str, message: str, msg_type: MessageType = MessageType.INFO):
        self.title = title
        self.message = message
        self.msg_type = msg_type
