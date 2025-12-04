import enum
import os

base_dir = os.path.dirname(__file__)


class PathType(enum.Enum):
    DIR = 0
    FILE = 1
