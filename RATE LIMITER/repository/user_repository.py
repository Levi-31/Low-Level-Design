from typing import Dict, Optional

from domain.user import User

class UserRepository:
    def __init__(self):
        self._users: Dict[str, User] = {}

    def save(self, user: User) -> None:
        self._users[user.user_id] = user

    def find_by_id(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)