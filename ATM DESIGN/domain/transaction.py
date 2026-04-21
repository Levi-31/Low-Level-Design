import time
from typing import Dict, Optional

from domain.denomination import Denomination
from domain.transaction_status import TransactionStatus
from domain.transaction_type import TransactionType

class Transaction:
    def __init__(self, id: str, atmId: str, sessionId: str, accountId: str, type: TransactionType, amountMinorUnits: int) -> None:
        self.id: str = id
        self.atmId: str = atmId
        self.sessionId: str = sessionId
        self.accountId: str = accountId
        self.type: TransactionType = type
        self.amountMinorUnits: int = amountMinorUnits
        self.status: TransactionStatus = TransactionStatus.PENDING
        self.dispensedNotes: Dict[Denomination, int] = {}
        self.depositedNotes: Dict[Denomination, int] = {}
        self.createdAt: int = int(time.time() * 1000)
        self.timeoutAt: int = self.createdAt + 300000

    # getters and setters 

    def getId(self) -> str:
        return self.id

    def setId(self, value: str) -> None:
        self.id = value

    def getAtmId(self) -> str:
        return self.atmId

    def setAtmId(self, value: str) -> None:
        self.atmId = value

    def getSessionId(self) -> str:
        return self.sessionId

    def setSessionId(self, value: str) -> None:
        self.sessionId = value

    def getAccountId(self) -> str:
        return self.accountId

    def setAccountId(self, value: str) -> None:
        self.accountId = value

    def getType(self) -> TransactionType:
        return self.type

    def setType(self, value: TransactionType) -> None:
        self.type = value

    def getAmountMinorUnits(self) -> int:
        return self.amountMinorUnits

    def setAmountMinorUnits(self, value: int) -> None:
        self.amountMinorUnits = value

    def getStatus(self) -> TransactionStatus:
        return self.status

    def setStatus(self, value: TransactionStatus) -> None:
        self.status = value

    def getDispensedNotes(self) -> Dict[Denomination, int]:
        return self.dispensedNotes

    def setDispensedNotes(self, value: Dict[Denomination, int]) -> None:
        self.dispensedNotes = dict(value)

    def getDepositedNotes(self) -> Dict[Denomination, int]:
        return self.depositedNotes

    def setDepositedNotes(self, value: Dict[Denomination, int]) -> None:
        self.depositedNotes = dict(value)

    def getCreatedAt(self) -> int:
        return self.createdAt

    def setCreatedAt(self, value: int) -> None:
        self.createdAt = value

    def getTimeoutAt(self) -> int:
        return self.timeoutAt

    def setTimeoutAt(self, value: int) -> None:
        self.timeoutAt = value
