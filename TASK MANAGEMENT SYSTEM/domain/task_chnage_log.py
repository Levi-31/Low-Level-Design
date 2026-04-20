from datetime import datetime

from domain.change_type import ChangeType


class TaskChangeLog:
    def __init__(self, id: int, task_id: int, user_id: int, change_type: ChangeType, old_value: str, new_value: str):
        self._id = id
        self._task_id = task_id
        self._user_id = user_id
        self._change_type = change_type
        self._old_value = old_value
        self._new_value = new_value
        self._timestamp = datetime.now()

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
    def change_type(self) -> ChangeType:
        return self._change_type

    @property
    def old_value(self) -> str:
        return self._old_value

    @property
    def new_value(self) -> str:
        return self._new_value

    @property
    def timestamp(self) -> datetime:
        return self._timestamp
