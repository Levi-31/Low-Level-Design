from typing import Optional, Dict, Any

from domain.cash_drawer import CashDrawer
from domain.state.idle_state import IdleState
from domain.state.support_notes import SupportsNotes
from domain.transaction import Transaction
from domain.transaction_type import TransactionType
from domain.denomination import Denomination
from domain.session import Session

# Import services with Any to prevent circular dependency if needed, or string type hints, but typing ANY is safe for cyclic imports here.
# We can use TYPE_CHECKING
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from service.card_service import CardService
    from service.session_service import SessionService
    from service.transaction_service import TransactionService
    from domain.state.abstract_atm_state import AbstractATMState

class ATM:
    def __init__(self, id: str, location: str) -> None:
        self.id: str = id
        self.location: str = location
        self.isOnline: bool = True
        self.currentState: 'AbstractATMState' = IdleState()
        self.cashDrawer: CashDrawer = CashDrawer(id)
        self.currentSession: Optional[Session] = None
        self.cardService: Optional['CardService'] = None
        self.sessionService: Optional['SessionService'] = None
        self.transactionService: Optional['TransactionService'] = None
        self.lastTransaction: Optional[Transaction] = None
    
    def attachServices(self, cardService: 'CardService', sessionService: 'SessionService', transactionService: 'TransactionService') -> None:
        self.cardService = cardService
        self.sessionService = sessionService
        self.transactionService = transactionService
    
    def getId(self) -> str:
        return self.id

    def setId(self, value: str) -> None:
        self.id = value

    def getLocation(self) -> str:
        return self.location

    def setLocation(self, value: str) -> None:
        self.location = value

    def getIsOnline(self) -> bool:
        return self.isOnline

    def setOnline(self, value: bool) -> None:
        self.isOnline = value

    def getCurrentState(self) -> 'AbstractATMState':
        return self.currentState

    def setCurrentState(self, value: 'AbstractATMState') -> None:
        self.currentState = value

    def getCashDrawer(self) -> CashDrawer:
        return self.cashDrawer

    def setCashDrawer(self, value: CashDrawer) -> None:
        self.cashDrawer = value

    def getCurrentSession(self) -> Optional[Session]:
        return self.currentSession

    def setCurrentSession(self, value: Optional[Session]) -> None:
        self.currentSession = value

    def getCardService(self) -> Optional['CardService']:
        return self.cardService

    def getSessionService(self) -> Optional['SessionService']:
        return self.sessionService

    def getTransactionService(self) -> Optional['TransactionService']:
        return self.transactionService

    def getLastTransaction(self) -> Optional[Transaction]:
        return self.lastTransaction

    def setLastTransaction(self, value: Optional[Transaction]) -> None:
        self.lastTransaction = value

# STATE PATTERN USED HERE 

    def insertCard(self, cardId: str) -> None:
        self.currentState.insertCard(self, cardId)
        self.autoNext()

    def ejectCard(self) -> None:
        self.currentState.ejectCard(self)
        self.autoNext()

    def enterPin(self, pin: str) -> None:
        self.currentState.enterPin(self, pin)
        self.autoNext()

    def selectTransaction(self, transactionType: TransactionType) -> None:
        self.currentState.selectTransaction(self, transactionType)
        self.autoNext()

    def processTransaction(self, amount: int, notes: Optional[Dict[Denomination, int]] = None) -> None:
        if notes is not None and isinstance(self.currentState, SupportsNotes):
            self.currentState.processTransactionWithNotes(self, amount, notes)
        else:
            self.currentState.processTransaction(self, amount)
        self.autoNext()

    def endSession(self) -> None:
        self.currentState.endSession(self)
        self.autoNext()

    def autoNext(self) -> None:
        nextState: Optional['AbstractATMState'] = self.currentState.next(self)
        if nextState is not None and nextState.__class__ != self.currentState.__class__:
            print(f"[STATE] {self.currentState.getStateName()} → {nextState.getStateName()}")
            self.currentState = nextState
