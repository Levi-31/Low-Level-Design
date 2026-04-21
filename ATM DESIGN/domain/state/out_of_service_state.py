from typing import Optional, TYPE_CHECKING
from domain.exception.invalid_atm_operation import InvalidATMOperationException
from domain.state.abstract_atm_state import AbstractATMState
from domain.state.ATMstate import ATMState

if TYPE_CHECKING:
    from domain.atm import ATM


class OutOfServiceState(AbstractATMState):
    def insertCard(self, atm: 'ATM', cardId: str) -> None:
        raise InvalidATMOperationException("ATM is out of service")

    def ejectCard(self, atm: 'ATM') -> None:
        print("[OutOfServiceState] ejectCard (if any)")

    def next(self, atm: 'ATM') -> Optional[ATMState]:
        return None