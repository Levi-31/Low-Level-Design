from typing import Dict, Optional
from repository.admin_repository import AdminUserRepositoryImpl
from repository.cash_drawer_repository import CashDrawerRepositoryImpl
from repository.transaction_repository import TransactionRepositoryImpl
from domain.cash_drawer import CashDrawer
from domain.denomination import Denomination

class AdminService:
    def __init__(self, adminUserRepository: AdminUserRepositoryImpl, cashDrawerRepository: CashDrawerRepositoryImpl, transactionRepository: TransactionRepositoryImpl) -> None:
        self.adminUserRepository = adminUserRepository
        self.cashDrawerRepository = cashDrawerRepository
        self.transactionRepository = transactionRepository

    def loginAdmin(self, adminId: str, pin: str) -> bool:
        admin = self.adminUserRepository.findById(adminId)
        return admin is not None and admin.isActiveUser() and admin.getPinHash() == pin

    def refillCash(self, atmId: str, notes: Dict[Denomination, int]) -> None:
        cashDrawer = self.cashDrawerRepository.findByATMId(atmId)
        if cashDrawer is not None:
            for denomination, count in notes.items():
                cashDrawer.addNotes(denomination, count)
            self.cashDrawerRepository.save(cashDrawer)
            print(f"[AdminService] Cash refilled for ATM: {atmId}")

    def auditCash(self, atmId: str) -> Optional[CashDrawer]:
        return self.cashDrawerRepository.findByATMId(atmId)
