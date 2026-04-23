



from typing import Dict, List, Optional

from domain.transaction import Transaction
from repository.transaction_repository import TransactionRepository


class TransactionRepositoryImpl(TransactionRepository):
    def __init__(self):
        self._transactions_by_id: Dict[str, Transaction] = {}
        self._transaction_id_by_provider_ref: Dict[str, str] = {}

    def save(self, transaction: Transaction) -> Transaction:
        self._transactions_by_id[transaction.id] = transaction
        if transaction.provider_ref:
            self._transaction_id_by_provider_ref[transaction.provider_ref] = transaction.id
        return transaction

    def find_by_id(self, transaction_id: str) -> Optional[Transaction]:
        return self._transactions_by_id.get(transaction_id)

    def find_by_provider_ref(self, provider_ref: str) -> Optional[Transaction]:
        tx_id = self._transaction_id_by_provider_ref.get(provider_ref)
        if tx_id is None:
            return None
        return self._transactions_by_id.get(tx_id)

    def find_by_wallet_and_range(self, wallet_id: str, start_utc: int, end_utc: int) -> List[Transaction]:
        result = [
            t for t in self._transactions_by_id.values()
            if (t.from_wallet_id == wallet_id or t.to_wallet_id == wallet_id)
            and start_utc <= t.timestamp <= end_utc
        ]
        result.sort(key=lambda t: t.timestamp)
        return result
