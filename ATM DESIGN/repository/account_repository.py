from typing import Dict, Optional
from domain.account import Account

class AccountRepositoryImpl:
    def __init__(self) -> None:
        self.accountStore: Dict[str, Account] = {}

    def save(self, account: Account) -> Account:
        self.accountStore[account.getId()] = account
        return account

    def findById(self, accountId: str) -> Optional[Account]:
        return self.accountStore.get(accountId)

    def updateBalance(self, accountId: str, newBalance: int) -> None:
        account = self.findById(accountId)
        if account is not None:
            account.setBalanceMinorUnits(newBalance)

    def updateDailyWithdrawalUsed(self, accountId: str, amountUsed: int) -> None:
        account = self.findById(accountId)
        if account is not None:
            account.setDailyWithdrawalUsedMinor(amountUsed)
