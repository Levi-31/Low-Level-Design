

from enum import Enum, auto


class PaymentType(Enum):
    PRE_PAYMENT = auto()
    POST_PAYMENT = auto()