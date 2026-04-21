class Card:
    def __init__(self, id: str, accountId: str, expiry: str) -> None:
        self.id: str = id 
        self.accountId: str = accountId
        self.expiry: str = expiry
        self.isBlocked: bool = False
        self.pinRetriesLeft: int = 3

    # GETTERS AND SETTERS 
    
    def getId(self) -> str:
        return self.id

    def setId(self, value: str) -> None:
        self.id = value

    def getAccountId(self) -> str:
        return self.accountId

    def setAccountId(self, value: str) -> None:
        self.accountId = value

    def getExpiry(self) -> str:
        return self.expiry

    def setExpiry(self, value: str) -> None:
        self.expiry = value

    def isBlockedCard(self) -> bool:
        return self.isBlocked

    def setBlocked(self, value: bool) -> None:
        self.isBlocked = value

    def getPinRetriesLeft(self) -> int:
        return self.pinRetriesLeft

    def setPinRetriesLeft(self, value: int) -> None:
        self.pinRetriesLeft = value

    def decrementPinRetries(self) -> None:
        self.pinRetriesLeft -= 1
        if self.pinRetriesLeft <= 0:
            self.isBlocked = True

    def resetPinRetries(self) -> None:
        self.pinRetriesLeft = 3
