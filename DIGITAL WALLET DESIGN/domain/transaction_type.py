

from enum import Enum, auto


class TransactionType(Enum):
    TRANSFER = auto()
    DEPOSIT = auto()
    WITHDRAWAL = auto()