from dataclasses import dataclass

from domain.user_role import UserRole

@dataclass
class User:
    id: str
    name: str
    email: str
    role: UserRole
    created_at: int