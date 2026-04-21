from typing import Optional
from repository.atm_repository import ATMRepositoryImpl
from repository.cash_drawer_repository import CashDrawerRepositoryImpl
from domain.atm import ATM
from domain.cash_drawer import CashDrawer
from domain.state.idle_state import IdleState
from domain.state.out_of_service_state import OutOfServiceState

class ATMService:
    def __init__(self, atmRepository: ATMRepositoryImpl, cashDrawerRepository: CashDrawerRepositoryImpl) -> None:
        self.atmRepository = atmRepository
        self.cashDrawerRepository = cashDrawerRepository

    def takeOffline(self, atmId: str) -> None:
        atm = self.atmRepository.findById(atmId)
        if atm is not None:
            atm.setOnline(False)
            atm.setCurrentState(OutOfServiceState())
            self.atmRepository.save(atm)

    def bringOnline(self, atmId: str) -> None:
        atm = self.atmRepository.findById(atmId)
        if atm is not None:
            atm.setOnline(True)
            atm.setCurrentState(IdleState())
            self.atmRepository.save(atm)

    def auditCash(self, atmId: str) -> Optional[CashDrawer]:
        return self.cashDrawerRepository.findByATMId(atmId)

    def getATM(self, atmId: str) -> Optional[ATM]:
        return self.atmRepository.findById(atmId)