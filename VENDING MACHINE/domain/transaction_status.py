from enum import Enum

class TransactionStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"

    def __str__(self):
        return self.value