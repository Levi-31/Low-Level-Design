


from abc import ABC, abstractmethod

from domain.change_type import ChangeType


class TaskSubscriber(ABC):
    @abstractmethod
    def update(self, task_id: int, change_type: ChangeType, old_value: str, new_value: str):
        pass