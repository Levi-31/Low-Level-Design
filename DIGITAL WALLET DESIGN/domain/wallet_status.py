from enum import Enum, auto


class WalletStatus(Enum):
    ACTIVE = auto()
    SUSPENDED = auto()
    CLOSED = auto()