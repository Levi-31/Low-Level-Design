

from abc import ABC, abstractmethod

from domain.change_type import ChangeType
from domain.observer.task_subscriber import TaskSubscriber


class TaskSubject(ABC):
    @abstractmethod
    def attach(self, subscriber: TaskSubscriber):
        pass
        
    @abstractmethod
    def detach(self, subscriber: TaskSubscriber):
        pass
        
    @abstractmethod
    def notify_subscribers(self, change_type: ChangeType, old_value: str, new_value: str):
        pass