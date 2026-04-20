



from domain.task_status import TaskStatus
from service.task_state_service import TaskStateService


class TaskStateController:
    def __init__(self, task_state_service: TaskStateService):
        self._task_state_service = task_state_service

    def update_task_status(self, task_id: int, new_status: TaskStatus):
        self._task_state_service.update_task_status(task_id, new_status)