


from typing import Dict, Optional

from domain.transaction import Transaction


class PaymentRepository:
    def __init__(self):
        self._transactions_by_id: Dict[str, Transaction] = {}
        self._transaction_id_by_provider_ref: Dict[str, str] = {}
        
    def save(self, transaction: Transaction) -> Transaction:
        self._transactions_by_id[transaction.id] = transaction
        if transaction.gateway_transaction_id:
            self._transaction_id_by_provider_ref[transaction.gateway_transaction_id] = transaction.id
        return transaction

    def find_by_id(self, transaction_id: str) -> Optional[Transaction]:
        return self._transactions_by_id.get(transaction_id)

    def find_by_gateway_transaction_id(self, gateway_transaction_id: str) -> Optional[Transaction]:
        tx_id = self._transaction_id_by_provider_ref.get(gateway_transaction_id)
        if tx_id is None:
            return None
        return self._transactions_by_id.get(tx_id)


