from typing import Dict, Optional
from domain.exception.invalid_atm_operation import InvalidATMOperationException
from domain.transaction_type import TransactionType
from domain.denomination import Denomination
from domain.transaction import Transaction
from service.atm_service import ATMService
from service.session_service import SessionService
from service.transaction_service import TransactionService

class TransactionController:
    def __init__(self, transactionService: TransactionService, sessionService: SessionService, atmService: ATMService) -> None:
        self.transactionService = transactionService
        self.sessionService = sessionService
        self.atmService = atmService
    
    def showBalance(self, sessionId: str) -> Optional[Transaction]:
        session = self.sessionService.getSession(sessionId)
        if session is None:
            return None
        atm = self.atmService.getATM(session.getAtmId())
        if atm is None:
            return None
        try:
            atm.selectTransaction(TransactionType.BALANCE)
            atm.processTransaction(0)
            return atm.getLastTransaction()
        except InvalidATMOperationException as exception:
            print(f"[ERROR] {exception}")
            return None
        
    def withdrawCash(self, sessionId: str, amountMinorUnits: int) -> Optional[Transaction]:
        session = self.sessionService.getSession(sessionId)
        if session is None:
            return None
        atm = self.atmService.getATM(session.getAtmId())
        if atm is None:
            return None
        try:
            atm.selectTransaction(TransactionType.WITHDRAW)
            atm.processTransaction(amountMinorUnits)
            return atm.getLastTransaction()
        except InvalidATMOperationException as exception:
            print(f"[ERROR] {exception}")
            return None

    def depositCash(self, sessionId: str, notes: Dict[Denomination, int]) -> Optional[Transaction]:
        session = self.sessionService.getSession(sessionId)
        if session is None:
            return None
        atm = self.atmService.getATM(session.getAtmId())
        if atm is None:
            return None
        amount = self.calculateAmount(notes)
        try:
            atm.selectTransaction(TransactionType.DEPOSIT)
            atm.processTransaction(amount, notes)
            return atm.getLastTransaction()
        except InvalidATMOperationException as exception:
            print(f"[ERROR] {exception}")
            return None

    def calculateAmount(self, notes: Dict[Denomination, int]) -> int:
        return sum(denomination.value * count for denomination, count in notes.items())
