class Account:
    def __init__(self, id: str, holderName: str, balanceMinorUnits: int) -> None:
        self.id: str = id
        self.holderName: str = holderName
        self.balanceMinorUnits: int = balanceMinorUnits
        self.dailyWithdrawalLimitMinor: int = 50000
        self.dailyWithdrawalUsedMinor: int = 0
        self.isActive: bool = True

    # Getters and Setters

    def getId(self) -> str:
        return self.id

    def setId(self, value: str) -> None:
        self.id = value

    def getHolderName(self) -> str:
        return self.holderName

    def setHolderName(self, value: str) -> None:
        self.holderName = value

    def getBalanceMinorUnits(self) -> int:
        return self.balanceMinorUnits

    def setBalanceMinorUnits(self, value: int) -> None:
        self.balanceMinorUnits = value

    def getDailyWithdrawalLimitMinor(self) -> int:
        return self.dailyWithdrawalLimitMinor

    def setDailyWithdrawalLimitMinor(self, value: int) -> None:
        self.dailyWithdrawalLimitMinor = value

    def getDailyWithdrawalUsedMinor(self) -> int:
        return self.dailyWithdrawalUsedMinor

    def setDailyWithdrawalUsedMinor(self, value: int) -> None:
        self.dailyWithdrawalUsedMinor = value

    def isActiveAccount(self) -> bool:
        return self.isActive

    def setActive(self, value: bool) -> None:
        self.isActive = value
