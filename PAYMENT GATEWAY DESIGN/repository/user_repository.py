
from typing import Dict, Optional
from domain.user import User

class UserRepository:
    def __init__(self):
        self._users_by_id: Dict[int, User] = {}

    def save(self, user: User) -> User:
        self._users_by_id[user.id] = user
        return user

    def find_by_id(self, user_id: int) -> Optional[User]:
        return self._users_by_id.get(user_id)