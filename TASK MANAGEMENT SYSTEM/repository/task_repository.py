
from abc import ABC, abstractmethod
from typing import List, Optional

from domain.task import Task
from domain.task_search_criteria import TaskSearchCriteria


class TaskRepository(ABC):
    @abstractmethod
    def save(self, task: Task) -> Task:
        pass
        
    @abstractmethod
    def find_by_id(self, task_id: int) -> Optional[Task]:
        pass
        
    @abstractmethod
    def find_by_assignee(self, assignee_id: int) -> List[Task]:
        pass
        
    @abstractmethod
    def find_by_parent_task(self, parent_task_id: int) -> List[Task]:
        pass
        
    @abstractmethod
    def search(self, criteria: TaskSearchCriteria) -> List[Task]:
        pass
