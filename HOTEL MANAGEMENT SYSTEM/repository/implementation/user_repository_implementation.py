


from typing import Optional, Dict
from domain.user import User
from repository.user_repository import UserRepository

class UserRepositoryImpl(UserRepository):
    def __init__(self):
        self.users: Dict[str, User] = {}

    def save(self, user: User) -> User:
        self.users[user.id] = user
        return user

    def find_by_id(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)