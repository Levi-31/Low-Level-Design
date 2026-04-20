
from abc import ABC, abstractmethod

from domain.task import Task
from domain.task_status import TaskStatus


class TaskState(ABC):
    @abstractmethod
    def can_transition_to(self, new_status: TaskStatus) -> bool:
        pass
        
    @abstractmethod
    def perform_transition(self, task: Task, new_status: TaskStatus):
        pass
        
    @abstractmethod
    def get_state_name(self) -> str:
        pass
