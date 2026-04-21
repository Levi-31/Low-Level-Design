import time
from typing import Optional
from repository.session_repository import SessionRepositoryImpl
from domain.session import Session


class SessionService:
    def __init__(self, sessionRepository: SessionRepositoryImpl) -> None:
        self.sessionRepository = sessionRepository

    def startSession(self, atmId: str, cardId: str) -> Session:
        accountId = "ACC_001"
        session = Session(f"SESSION_{int(time.time() * 1000)}", atmId, cardId, accountId)
        return self.sessionRepository.save(session)

    def endSession(self, sessionId: str) -> None:
        self.sessionRepository.endSession(sessionId)

    def getCurrentSession(self, atmId: str) -> Optional[Session]:
        return self.sessionRepository.findActiveByATM(atmId)

    def handleSessionTimeout(self, sessionId: str) -> None:
        self.endSession(sessionId)

    def getSession(self, sessionId: str) -> Optional[Session]:
        return self.sessionRepository.findById(sessionId)
