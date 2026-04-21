class AdminUser:
    def __init__(self, id: str, name: str, pinHash: str) -> None:
        self.id: str = id
        self.name: str = name
        self.pinHash: str = pinHash
        self.isActive: bool = True

    def getId(self) -> str:
        return self.id

    def setId(self, value: str) -> None:
        self.id = value

    def getName(self) -> str:
        return self.name

    def setName(self, value: str) -> None:
        self.name = value

    def getPinHash(self) -> str:
        return self.pinHash

    def setPinHash(self, value: str) -> None:
        self.pinHash = value

    def isActiveUser(self) -> bool:
        return self.isActive

    def setActive(self, value: bool) -> None:
        self.isActive = value
