from typing import Optional
from domain.exception.invalid_atm_operation import InvalidATMOperationException
from domain.session import Session
from service.atm_service import ATMService
from service.session_service import SessionService

class SessionController:
    def __init__(self, sessionService: SessionService, atmService: ATMService) -> None:
        self.sessionService = sessionService
        self.atmService = atmService

    def startSession(self, atmId: str, cardId: str) -> Optional[Session]:
        atm = self.atmService.getATM(atmId)
        if atm is None:
            return None
        print("[SessionController] startSession handled by state during insertCard")
        return atm.getCurrentSession()

    def endSession(self, sessionId: str) -> None:
        session = self.sessionService.getSession(sessionId)
        if session is None:
            return
        atm = self.atmService.getATM(session.getAtmId())
        if atm is None:
            return
        try:
            atm.endSession()
        except InvalidATMOperationException as exception:
            print(f"[ERROR] {exception}")
