

from enum import Enum


class TransactionType(Enum):
    WITHDRAW = "WITHDRAW"
    DEPOSIT = "DEPOSIT"
    BALANCE = "BALANCE"

    