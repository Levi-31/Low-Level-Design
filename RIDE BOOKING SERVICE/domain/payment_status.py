from enum import Enum, auto


class PaymentStatus(Enum):
    NONE = auto()
    PENDING = auto()
    COMPLETED = auto()
    FAILED = auto()
    REFUNDED = auto()