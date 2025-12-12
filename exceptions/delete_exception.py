class DeleteException(Exception):
    def __init__(self, message: str, pth: str):
        super().__init__(message)
        self.pth = pth
