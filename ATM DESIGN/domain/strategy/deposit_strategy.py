import time
from typing import Dict, Optional

from domain.denomination import Denomination
from domain.strategy.transaction_strategy import TransactionStrategy
from domain.transaction import Transaction
from domain.transaction_status import TransactionStatus
from domain.transaction_type import TransactionType


class DepositStrategy(TransactionStrategy):
    def processTransaction(self, sessionId: str, amount: int, notes: Optional[Dict[Denomination, int]]) -> Transaction:
        print(f"[DepositStrategy] Processing deposit: {amount} for session: {sessionId}")
        transaction = Transaction(
            f"TXN_{int(time.time() * 1000)}",
            "ATM_001",
            sessionId,
            "ACC_001",
            TransactionType.DEPOSIT,
            amount,
        )
        if notes is not None:
            transaction.setDepositedNotes(notes)
        transaction.setStatus(TransactionStatus.SUCCESS)
        print(f"[DepositStrategy] Deposit completed, deposited: {notes}")
        return transaction
