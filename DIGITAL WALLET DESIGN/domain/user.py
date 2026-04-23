


class User:
    def __init__(self, id: str, username: str, email: str, name: str, created_at: int):
        self._id = id
        self._username = username
        self._email = email
        self._name = name
        self._created_at = created_at

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str):
        self._id = value

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value: str):
        self._username = value

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        self._email = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def created_at(self) -> int:
        return self._created_at

    @created_at.setter
    def created_at(self, value: int):
        self._created_at = value

    def __repr__(self) -> str:
        return (f"User{{id='{self._id}', username='{self._username}', "
                f"email='{self._email}', name='{self._name}'}}")
