

from domain.change_type import ChangeType
from domain.observer.task_subscriber import TaskSubscriber


class EmailSubscriber(TaskSubscriber):
    def __init__(self, email_address: str):
        self._email_address = email_address

    def update(self, task_id: int, change_type: ChangeType, old_value: str, new_value: str):
        print(f"[Email to {self._email_address}] Task {task_id} updated ({change_type.name}): {old_value} -> {new_value}")
