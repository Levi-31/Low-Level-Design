




from typing import List

from domain.change_type import ChangeType
from domain.task_chnage_log import TaskChangeLog
from domain.task_subscription import TaskSubscription
from repository.task_chnage_log_repository import TaskChangeLogRepository
from repository.task_subscription_repository import TaskSubscriptionRepository


class TaskNotificationService:
    def __init__(self, subscription_repository: TaskSubscriptionRepository, change_log_repository: TaskChangeLogRepository):
        self._subscription_repository = subscription_repository
        self._change_log_repository = change_log_repository

    def subscribe_to_task(self, task_id: int, user_id: int):
        sub = TaskSubscription(0, user_id, task_id)
        self._subscription_repository.save(sub)

    def unsubscribe_from_task(self, task_id: int, user_id: int):
        user_subs = self._subscription_repository.find_by_user_id(user_id)
        for sub in user_subs:
            if sub.task_id == task_id:
                sub.is_active = False
                self._subscription_repository.save(sub)
                break
            
    def notify_subscribers(self, task_id: int, change_type: ChangeType, old_value: str, new_value: str):
        log = TaskChangeLog(0, task_id, 0, change_type, old_value, new_value) # 0 for system actor
        self._change_log_repository.save(log)

    def get_task_history(self, task_id: int) -> List[TaskChangeLog]:
        return self._change_log_repository.find_by_task_id(task_id)