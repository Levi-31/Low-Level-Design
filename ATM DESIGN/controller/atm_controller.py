from typing import Optional
from domain.cash_drawer import CashDrawer
from service.atm_service import ATMService

class ATMController:
    def __init__(self, atmService: ATMService) -> None:
        self.atmService = atmService

    def takeOffline(self, atmId: str) -> None:
        self.atmService.takeOffline(atmId)

    def bringOnline(self, atmId: str) -> None:
        self.atmService.bringOnline(atmId)

    def auditCash(self, atmId: str) -> Optional[CashDrawer]:
        return self.atmService.auditCash(atmId)