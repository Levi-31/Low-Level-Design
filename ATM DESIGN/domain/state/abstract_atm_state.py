from typing import Optional, TYPE_CHECKING

from domain.exception.invalid_atm_operation import InvalidATMOperationException
from domain.state.ATMstate import ATMState
from domain.transaction_type import TransactionType

if TYPE_CHECKING:
    from domain.atm import ATM


class AbstractATMState(ATMState):
    def insertCard(self, atm: 'ATM', cardId: str) -> None:
        raise InvalidATMOperationException(f"Operation not allowed in {self.getStateName()}")

    def ejectCard(self, atm: 'ATM') -> None:
        raise InvalidATMOperationException(f"Operation not allowed in {self.getStateName()}")

    def enterPin(self, atm: 'ATM', pin: str) -> None:
        raise InvalidATMOperationException(f"Operation not allowed in {self.getStateName()}")

    def selectTransaction(self, atm: 'ATM', type: TransactionType) -> None:
        raise InvalidATMOperationException(f"Operation not allowed in {self.getStateName()}")

    def processTransaction(self, atm: 'ATM', amount: int) -> None:
        raise InvalidATMOperationException(f"Operation not allowed in {self.getStateName()}")

    def endSession(self, atm: 'ATM') -> None:
        raise InvalidATMOperationException(f"Operation not allowed in {self.getStateName()}")

    def next(self, atm: 'ATM') -> Optional[ATMState]:
        return None
