from typing import List

from domain.task_chnage_log import TaskChangeLog
from service.task_notification_service import TaskNotificationService


class TaskNotificationController:
    def __init__(self, task_notification_service: TaskNotificationService):
        self._task_notification_service = task_notification_service

    def subscribe_to_task(self, task_id: int, user_id: int):
        self._task_notification_service.subscribe_to_task(task_id, user_id)

    def unsubscribe_from_task(self, task_id: int, user_id: int):
        self._task_notification_service.unsubscribe_from_task(task_id, user_id)

    def get_task_history(self, task_id: int) -> List[TaskChangeLog]:
        return self._task_notification_service.get_task_history(task_id)