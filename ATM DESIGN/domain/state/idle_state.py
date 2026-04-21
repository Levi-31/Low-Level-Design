from typing import Optional, TYPE_CHECKING
from domain.state.abstract_atm_state import AbstractATMState
from domain.state.ATMstate import ATMState

if TYPE_CHECKING:
    from domain.atm import ATM

class IdleState(AbstractATMState):
    def insertCard(self, atm: 'ATM', cardId: str) -> None:
        print(f"[IdleState] insertCard: {cardId}")
        cardService = atm.getCardService()
        if cardService is not None:
            print("[CardService] validate card and cache details")
        sessionService = atm.getSessionService()
        if sessionService is not None:
            print("[SessionService] start session")
            atm.setCurrentSession(sessionService.startSession(atm.getId(), cardId))

    def next(self, atm: 'ATM') -> Optional[ATMState]:
        if atm.getCurrentSession() is not None:
            from domain.state.card_inserted_state import CardInsertedState
            return CardInsertedState()
        return None