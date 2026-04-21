import time
from typing import Dict, Optional

from domain.denomination import Denomination
from domain.strategy.transaction_strategy import TransactionStrategy
from domain.transaction import Transaction
from domain.transaction_status import TransactionStatus
from domain.transaction_type import TransactionType


class WithdrawalStrategy(TransactionStrategy):
    def processTransaction(self, sessionId: str, amount: int, notes: Optional[Dict[Denomination, int]]) -> Transaction:
        print(f"[WithdrawalStrategy] Processing withdrawal: {amount} for session: {sessionId}")
        transaction = Transaction(
            f"TXN_{int(time.time() * 1000)}",
            "ATM_001",
            sessionId,
            "ACC_001",
            TransactionType.WITHDRAW,
            amount,
        )
        transaction.setDispensedNotes(self.calculateNotes(amount))
        transaction.setStatus(TransactionStatus.SUCCESS)
        print(f"[WithdrawalStrategy] Withdrawal completed, dispensed: {transaction.getDispensedNotes()}")
        return transaction

    def calculateNotes(self, amount: int) -> Dict[Denomination, int]:
        notes: Dict[Denomination, int] = {}
        remaining = amount
        for denomination in Denomination:
            count = remaining // denomination.value
            if count > 0:
                notes[denomination] = count
                remaining -= count * denomination.value
        return notes
