from typing import Optional, TYPE_CHECKING
from domain.exception.invalid_atm_operation import InvalidATMOperationException
from domain.state.abstract_atm_state import AbstractATMState
from domain.state.ATMstate import ATMState

if TYPE_CHECKING:
    from domain.atm import ATM


class CardInsertedState(AbstractATMState):
    def insertCard(self, atm: 'ATM', cardId: str) -> None:
        raise InvalidATMOperationException("Card already inserted")

    def ejectCard(self, atm: 'ATM') -> None:
        print("[CardInsertedState] ejectCard")
        sessionService = atm.getSessionService()
        if sessionService is not None and atm.getCurrentSession() is not None:
            print("[SessionService] end session")
            sessionService.endSession(atm.getCurrentSession().getId())
            atm.setCurrentSession(None)

    def enterPin(self, atm: 'ATM', pin: str) -> None:
        print("[CardInsertedState] enterPin")
        cardService = atm.getCardService()
        ok = True
        if cardService is not None and atm.getCurrentSession() is not None:
            print("[CardService] authenticate card")
            ok = cardService.authenticateCard(atm.getCurrentSession().getCardId(), pin)
        if not ok:
            raise InvalidATMOperationException("Authentication failed")

    def endSession(self, atm: 'ATM') -> None:
        print("[CardInsertedState] endSession")
        sessionService = atm.getSessionService()
        if sessionService is not None and atm.getCurrentSession() is not None:
            sessionService.endSession(atm.getCurrentSession().getId())
            atm.setCurrentSession(None)

    def next(self, atm: 'ATM') -> Optional[ATMState]:
        if atm.getCurrentSession() is None:
            from domain.state.idle_state import IdleState
            return IdleState()
        from domain.state.authenticated_state import AuthenticatedState
        return AuthenticatedState()
