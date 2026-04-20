from typing import List

from domain.strategy.task_sorting_strategy import TaskSortingStrategy
from domain.task import Task


class DueDateSortingStrategy(TaskSortingStrategy):
    def sort(self, tasks: List[Task]) -> List[Task]:
        return sorted(tasks, key=lambda t: t._due_date)

    def get_strategy_name(self) -> str:
        return "DUE_DATE"
    
    