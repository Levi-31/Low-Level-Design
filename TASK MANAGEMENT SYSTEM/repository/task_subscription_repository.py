

from typing import Dict, List

from domain.task_subscription import TaskSubscription


class TaskSubscriptionRepository:
    def __init__(self):
        self._subscriptions: Dict[int, TaskSubscription] = {}
        self._next_id = 1
    

    def save(self, subscription: TaskSubscription) -> TaskSubscription:
        if subscription.id == 0:
            new_sub = TaskSubscription(self._next_id, subscription.user_id, subscription.task_id)
            self._next_id += 1
            self._subscriptions[new_sub.id] = new_sub
            return new_sub
            
        self._subscriptions[subscription.id] = subscription
        return subscription
    
    def find_by_task_id(self, task_id: int) -> List[TaskSubscription]:
        return [s for s in self._subscriptions.values() if s.task_id == task_id and s.is_active]

    def find_by_user_id(self, user_id: int) -> List[TaskSubscription]:
        return [s for s in self._subscriptions.values() if s.user_id == user_id and s.is_active]