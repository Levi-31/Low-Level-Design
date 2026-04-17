from typing import Dict, List, Optional
from domain.transaction import Transaction

class PaymentRepository:
    def __init__(self):
        self._transactions: Dict[int, Transaction] = {}

    def save(self, transaction: Transaction):
        self._transactions[transaction.id] = transaction

    def find_by_id(self, transaction_id: int) -> Optional[Transaction]:
        return self._transactions.get(transaction_id)

    def find_all_by_machine_id(self, machine_id: int) -> List[Transaction]:
        return [t for t in self._transactions.values() if t.vending_machine_id == machine_id]
