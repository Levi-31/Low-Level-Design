

from domain.user_role import UserRole


class User:
    def __init__(self, id: int, username: str, email: str, role: UserRole):
        self._id = id
        self._username = username
        self._email = email
        self._role = role

    @property
    def id(self) -> int:
        return self._id

    @property
    def username(self) -> str:
        return self._username

    @property
    def email(self) -> str:
        return self._email

    @property
    def role(self) -> UserRole:
        return self._role
