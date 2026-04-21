from typing import Dict, Optional
from domain.cash_drawer import CashDrawer
from domain.denomination import Denomination
from service.admin_service import AdminService

class AdminController:
    def __init__(self, adminService: AdminService) -> None:
        self.adminService = adminService

    def loginAdmin(self, adminId: str, pin: str) -> bool:
        return self.adminService.loginAdmin(adminId, pin)

    def refillCash(self, atmId: str, notes: Dict[Denomination, int]) -> None:
        self.adminService.refillCash(atmId, notes)

    def auditCash(self, atmId: str) -> Optional[CashDrawer]:
        return self.adminService.auditCash(atmId)