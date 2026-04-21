from typing import Dict, List, Optional
from domain.atm import ATM
from domain.state.abstract_atm_state import AbstractATMState

class ATMRepositoryImpl:
    def __init__(self) -> None:
        self.atmStore: Dict[str, ATM] = {}

    def save(self, atm: ATM) -> ATM:
        self.atmStore[atm.getId()] = atm
        return atm

    def findById(self, atmId: str) -> Optional[ATM]:
        return self.atmStore.get(atmId)

    def findAll(self) -> List[ATM]:
        return list(self.atmStore.values())

    def updateATMState(self, atmId: str, state: AbstractATMState) -> None:
        atm = self.findById(atmId)
        if atm is not None:
            atm.setCurrentState(state)
