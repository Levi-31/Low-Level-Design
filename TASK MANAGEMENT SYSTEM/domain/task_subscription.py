class TaskSubscription:
    def __init__(self, id: int, user_id: int, task_id: int):
        self._id = id
        self._user_id = user_id
        self._task_id = task_id
        self._is_active = True

    @property
    def id(self) -> int:
        return self._id

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def task_id(self) -> int:
        return self._task_id

    @property
    def is_active(self) -> bool:
        return self._is_active
        
    @is_active.setter
    def is_active(self, value: bool):
        self._is_active = value
