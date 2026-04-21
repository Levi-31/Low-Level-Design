from typing import Dict, Optional
from domain.session import Session


class SessionRepositoryImpl:
    def __init__(self) -> None:
        self.sessionStore: Dict[str, Session] = {}

    def save(self, session: Session) -> Session:
        self.sessionStore[session.getId()] = session
        return session

    def findById(self, sessionId: str) -> Optional[Session]:
        return self.sessionStore.get(sessionId)

    def findActiveByATM(self, atmId: str) -> Optional[Session]:
        for session in self.sessionStore.values():
            if session.getAtmId() == atmId and session.isActiveSession():
                return session
        return None

    def endSession(self, sessionId: str) -> None:
        session = self.findById(sessionId)
        if session is not None:
            session.endSession()
