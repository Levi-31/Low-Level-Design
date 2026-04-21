from abc import ABC, abstractmethod
from typing import Dict, Optional
from domain.denomination import Denomination
from domain.transaction import Transaction


class TransactionStrategy(ABC):
    @abstractmethod
    def processTransaction(self, sessionId: str, amount: int, notes: Optional[Dict[Denomination, int]]) -> Transaction:
        pass