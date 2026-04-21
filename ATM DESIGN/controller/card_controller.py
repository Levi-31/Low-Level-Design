from domain.exception.invalid_atm_operation import InvalidATMOperationException
from service.atm_service import ATMService

class CardController:
    def __init__(self, atmService: ATMService) -> None:
        self.atmService = atmService

    def insertCard(self, atmId: str, cardId: str) -> bool:
        atm = self.atmService.getATM(atmId)
        if atm is None:
            return False
        try:
            atm.insertCard(cardId)
            return True
        except InvalidATMOperationException as exception:
            print(f"[ERROR] {exception}")
            return False

    def ejectCard(self, atmId: str) -> None:
        atm = self.atmService.getATM(atmId)
        if atm is None:
            return
        try:
            atm.ejectCard()
        except InvalidATMOperationException as exception:
            print(f"[ERROR] {exception}")

    def authenticateCard(self, atmId: str, cardId: str, pin: str) -> bool:
        atm = self.atmService.getATM(atmId)
        if atm is None:
            return False
        try:
            atm.enterPin(pin)
            return True
        except InvalidATMOperationException as exception:
            print(f"[ERROR] {exception}")
            return False
