import time
from typing import Optional
from domain.transaction_type import TransactionType

class Session:
    def __init__(self, id: str, atmId: str, cardId: str, accountId: str) -> None:
        self.id: str = id
        self.atmId: str = atmId
        self.cardId: str = cardId
        self.accountId: str = accountId
        self.startTime: int = int(time.time() * 1000)
        self.endTime: int = 0
        self.isActive: bool = True
        self.currentTransactionId: Optional[str] = None
        self.transactionType: Optional[TransactionType] = None
        self.amount: int = 0

    def getId(self) -> str:
        return self.id

    def setId(self, value: str) -> None:
        self.id = value

    def getAtmId(self) -> str:
        return self.atmId

    def setAtmId(self, value: str) -> None:
        self.atmId = value

    def getCardId(self) -> str:
        return self.cardId

    def setCardId(self, value: str) -> None:
        self.cardId = value

    def getAccountId(self) -> str:
        return self.accountId

    def setAccountId(self, value: str) -> None:
        self.accountId = value

    def getStartTime(self) -> int:
        return self.startTime

    def setStartTime(self, value: int) -> None:
        self.startTime = value

    def getEndTime(self) -> int:
        return self.endTime

    def setEndTime(self, value: int) -> None:
        self.endTime = value

    def isActiveSession(self) -> bool:
        return self.isActive

    def setActive(self, value: bool) -> None:
        self.isActive = value

    def getCurrentTransactionId(self) -> Optional[str]:
        return self.currentTransactionId

    def setCurrentTransactionId(self, value: Optional[str]) -> None:
        self.currentTransactionId = value

    def getTransactionType(self) -> Optional[TransactionType]:
        return self.transactionType

    def setTransactionType(self, value: Optional[TransactionType]) -> None:
        self.transactionType = value

    def transactionTypePresent(self) -> bool:
        return self.transactionType is not None

    def clearTransactionType(self) -> None:
        self.transactionType = None

    def getAmount(self) -> int:
        return self.amount

    def setAmount(self, value: int) -> None:
        self.amount = value

    def endSession(self) -> None:
        self.isActive = False
        self.endTime = int(time.time() * 1000)
