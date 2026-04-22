


from typing import Dict, Optional

from domain.transaction import Transaction
from repository.transaction_repository import TransactionRepository


class TransactionRepositoryImpl(TransactionRepository):
    def __init__(self):
        self.transactions: Dict[str, Transaction] = {}
        self.provider_ref_to_id: Dict[str, str] = {} # reference_id to id mapping 

    def save(self, transaction: Transaction) -> Transaction:
        self.transactions[transaction.id] = transaction
        if transaction.provider_ref:
            self.provider_ref_to_id[transaction.provider_ref] = transaction.id
        return transaction

    def find_by_provider_ref(self, provider_ref: str) -> Optional[Transaction]:
        transaction_id = self.provider_ref_to_id.get(provider_ref)
        if not transaction_id:
            return None
        return self.transactions.get(transaction_id)