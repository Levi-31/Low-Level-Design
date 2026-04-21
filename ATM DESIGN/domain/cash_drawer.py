from typing import Dict
from domain.denomination import Denomination

class CashDrawer:
    def __init__(self, atmId: str) -> None:
        self.atmId: str = atmId
        self.notesByDenomination: Dict[Denomination, int] = {denomination: 0 for denomination in Denomination}
    
    def getAtmId(self) -> str:
        return self.atmId

    def setAtmId(self, value: str) -> None:
        self.atmId = value

    def getNotesByDenomination(self) -> Dict[Denomination, int]:
        return self.notesByDenomination

    def setNotesByDenomination(self, value: Dict[Denomination, int]) -> None:
        self.notesByDenomination = dict(value)

    def addNotes(self, denomination: Denomination, count: int) -> None:
        self.notesByDenomination[denomination] = self.notesByDenomination.get(denomination, 0) + count

    def removeNotes(self, denomination: Denomination, count: int) -> None:
        self.notesByDenomination[denomination] = max(0, self.notesByDenomination.get(denomination, 0) - count)

    def getTotalCash(self) -> int:
        return sum(denomination.value * count for denomination, count in self.notesByDenomination.items())