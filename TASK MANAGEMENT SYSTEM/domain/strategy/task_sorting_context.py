

from typing import List, Optional

from domain.strategy.task_sorting_strategy import TaskSortingStrategy
from domain.task import Task


class TaskSortingContext:
    def __init__(self, strategy: Optional[TaskSortingStrategy] = None):
        self._strategy = strategy
        
    def set_sorting_strategy(self, strategy: TaskSortingStrategy):
        self._strategy = strategy
        
    def sort_tasks(self, tasks: List[Task]) -> List[Task]:
        if not self._strategy:
            return tasks
        return self._strategy.sort(tasks)
