

from abc import ABC, abstractmethod
from typing import Optional
from domain.user import User


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional[User]:
        pass