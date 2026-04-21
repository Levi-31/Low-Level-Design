from typing import Dict, List, Optional
from domain.transaction import Transaction
from domain.transaction_status import TransactionStatus

class TransactionRepositoryImpl:
    def __init__(self) -> None:
        self.transactionStore: Dict[str, Transaction] = {}

    def save(self, transaction: Transaction) -> Transaction:
        self.transactionStore[transaction.getId()] = transaction
        return transaction

    def findById(self, transactionId: str) -> Optional[Transaction]:
        return self.transactionStore.get(transactionId)

    def findBySession(self, sessionId: str) -> List[Transaction]:
        return [transaction for transaction in self.transactionStore.values() if transaction.getSessionId() == sessionId]

    def findByATMAndTimeRange(self, atmId: str, startTime: int, endTime: int) -> List[Transaction]:
        return [
            transaction
            for transaction in self.transactionStore.values()
            if transaction.getAtmId() == atmId and startTime <= transaction.getCreatedAt() <= endTime
        ]

    def updateTransactionStatus(self, transactionId: str, status: TransactionStatus) -> None:
        transaction = self.findById(transactionId)
        if transaction is not None:
            transaction.setStatus(status)
