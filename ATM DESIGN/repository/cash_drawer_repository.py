from typing import Dict, Optional
from domain.cash_drawer import CashDrawer
from domain.denomination import Denomination

class CashDrawerRepositoryImpl:
    def __init__(self) -> None:
        self.cashDrawerStore: Dict[str, CashDrawer] = {}

    def save(self, cashDrawer: CashDrawer) -> CashDrawer:
        self.cashDrawerStore[cashDrawer.getAtmId()] = cashDrawer
        return cashDrawer

    def findByATMId(self, atmId: str) -> Optional[CashDrawer]:
        return self.cashDrawerStore.get(atmId)

    def updateCashInventory(self, atmId: str, notes: Dict[Denomination, int]) -> None:
        cashDrawer = self.findByATMId(atmId)
        if cashDrawer is not None:
            cashDrawer.setNotesByDenomination(notes)
