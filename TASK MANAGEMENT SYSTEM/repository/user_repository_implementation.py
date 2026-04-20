from typing import Dict, Optional

from domain.user import User
from domain.user_role import UserRole
from repository.user_repository import UserRepository


class UserRepositoryImpl(UserRepository):
    def __init__(self):
        self._users: Dict[int, User] = {
            1: User(1, "alice", "alice@example.com", UserRole.ADMIN),
            2: User(2, "bob", "bob@example.com", UserRole.USER)
        }

    def find_by_id(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)
    