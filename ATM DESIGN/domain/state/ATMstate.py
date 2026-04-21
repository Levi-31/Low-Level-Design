from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from domain.transaction_type import TransactionType

if TYPE_CHECKING:
    from domain.atm import ATM

class ATMState(ABC):
    @abstractmethod
    def insertCard(self, atm: 'ATM', cardId: str) -> None:
        pass

    @abstractmethod
    def ejectCard(self, atm: 'ATM') -> None:
        pass

    @abstractmethod
    def enterPin(self, atm: 'ATM', pin: str) -> None:
        pass

    @abstractmethod
    def selectTransaction(self, atm: 'ATM', type: TransactionType) -> None:
        pass

    @abstractmethod
    def processTransaction(self, atm: 'ATM', amount: int) -> None:
        pass

    @abstractmethod
    def endSession(self, atm: 'ATM') -> None:
        pass

    @abstractmethod
    def next(self, atm: 'ATM') -> 'ATMState':
        pass

    def getStateName(self) -> str:
        return self.__class__.__name__
