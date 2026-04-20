from datetime import datetime

class Comment:
    def __init__(self, id: int, task_id: int, user_id: int, content: str):
        self._id = id
        self._task_id = task_id
        self._user_id = user_id
        self._content = content
        self._created_at = datetime.now()

    @property
    def id(self) -> int:
        return self._id

    @property
    def task_id(self) -> int:
        return self._task_id

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def content(self) -> str:
        return self._content

    @property
    def created_at(self) -> datetime:
        return self._created_at
