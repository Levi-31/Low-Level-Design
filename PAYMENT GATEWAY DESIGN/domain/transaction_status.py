

from enum import Enum, auto


class TransactionStatus(Enum):
    INITIATED = auto()
    PENDING = auto()
    SUCCESS = auto()
    FAILED = auto()
    CANCELLED = auto()