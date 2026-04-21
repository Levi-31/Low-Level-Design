from typing import Optional, TYPE_CHECKING
from domain.exception.invalid_atm_operation import InvalidATMOperationException
from domain.state.abstract_atm_state import AbstractATMState
from domain.state.ATMstate import ATMState
from domain.transaction_type import TransactionType

if TYPE_CHECKING:
    from domain.atm import ATM


class AuthenticatedState(AbstractATMState):
    def insertCard(self, atm: 'ATM', cardId: str) -> None:
        raise InvalidATMOperationException("Card already inserted")

    def ejectCard(self, atm: 'ATM') -> None:
        print("[AuthenticatedState] ejectCard")
        self.endSession(atm)

    def enterPin(self, atm: 'ATM', pin: str) -> None:
        raise InvalidATMOperationException("Already authenticated")

    def selectTransaction(self, atm: 'ATM', type: TransactionType) -> None:
        print(f"[AuthenticatedState] selectTransaction: {type.name}")
        if atm.getCurrentSession() is not None:
            atm.getCurrentSession().setTransactionType(type)

    def endSession(self, atm: 'ATM') -> None:
        print("[AuthenticatedState] endSession")
        sessionService = atm.getSessionService()
        if sessionService is not None and atm.getCurrentSession() is not None:
            sessionService.endSession(atm.getCurrentSession().getId())
            atm.setCurrentSession(None)

    def next(self, atm: 'ATM') -> Optional[ATMState]:
        from domain.state.transaction_selected_state import TransactionSelectedState
        if atm.getCurrentSession() is not None and atm.getCurrentSession().transactionTypePresent():
            return TransactionSelectedState()
        return None