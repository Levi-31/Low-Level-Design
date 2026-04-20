

from abc import ABC, abstractmethod
from typing import List

from domain.task import Task


class TaskSortingStrategy(ABC):
    @abstractmethod
    def sort(self, tasks: List[Task]) -> List[Task]:
        pass
        
    @abstractmethod
    def get_strategy_name(self) -> str:
        pass


    