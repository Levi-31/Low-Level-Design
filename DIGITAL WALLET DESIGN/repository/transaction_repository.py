


from abc import ABC, abstractmethod
from typing import Optional
from domain.transaction import Transaction
from typing import List


class TransactionRepository(ABC):
    @abstractmethod
    def save(self, transaction: Transaction) -> Transaction:
        pass

    @abstractmethod
    def find_by_id(self, transaction_id: str) -> Optional[Transaction]:
        pass

    @abstractmethod
    def find_by_provider_ref(self, provider_ref: str) -> Optional[Transaction]:
        pass

    @abstractmethod
    def find_by_wallet_and_range(self, wallet_id: str, start_utc: int, end_utc: int) -> List[Transaction]:
        pass