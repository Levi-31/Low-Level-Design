from enum import Enum, auto

class ChangeType(Enum):
    CREATED = auto()
    UPDATED = auto()
    STATUS_CHANGED = auto()
    ASSIGNED = auto()
    PRIORITY_CHANGED = auto()
