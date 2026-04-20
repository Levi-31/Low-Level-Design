


from domain.change_type import ChangeType
from domain.observer.task_subscriber import TaskSubscriber


class MobileAppSubscriber(TaskSubscriber):
    def __init__(self, device_token: str):
        self._device_token = device_token

    def update(self, task_id: int, change_type: ChangeType, old_value: str, new_value: str):
        print(f"[Push Notification to {self._device_token}] Task {task_id} updated ({change_type.name}): {old_value} -> {new_value}")
