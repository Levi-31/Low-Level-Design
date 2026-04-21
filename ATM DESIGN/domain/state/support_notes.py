from abc import ABC, abstractmethod
from typing import Dict, TYPE_CHECKING
from domain.denomination import Denomination

if TYPE_CHECKING:
    from domain.atm import ATM

class SupportsNotes(ABC):
    @abstractmethod
    def processTransactionWithNotes(self, atm: 'ATM', amount: int, notes: Dict[Denomination, int]) -> None:
        pass