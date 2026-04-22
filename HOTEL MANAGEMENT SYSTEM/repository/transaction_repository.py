

from abc import ABC , abstractmethod
from typing import Optional
from domain.transaction import Transaction

class TransactionRepository(ABC):
    @abstractmethod
    def save(self, transaction: Transaction) -> Transaction:
        pass

    @abstractmethod
    def find_by_provider_ref(self, provider_ref: str) -> Optional[Transaction]:
        pass