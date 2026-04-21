from typing import Dict, Optional
from domain.admin_user import AdminUser

class AdminUserRepositoryImpl:
    def __init__(self) -> None:
        self.adminStore: Dict[str, AdminUser] = {}

    def save(self, adminUser: AdminUser) -> AdminUser:
        self.adminStore[adminUser.getId()] = adminUser
        return adminUser

    def findById(self, adminId: str) -> Optional[AdminUser]:
        return self.adminStore.get(adminId)

    def validateAdminCredentials(self, adminId: str, pinHash: str) -> bool:
        admin = self.findById(adminId)
        return admin is not None and admin.isActiveUser() and admin.getPinHash() == pinHash
