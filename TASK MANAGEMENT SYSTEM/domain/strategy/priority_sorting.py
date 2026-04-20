




from typing import List

from domain.strategy.task_sorting_strategy import TaskSortingStrategy
from domain.task import Task


class PrioritySortingStrategy(TaskSortingStrategy):
    def sort(self, tasks: List[Task]) -> List[Task]:
        # Sort descending essentially: URGENT(4) > HIGH(3) > MEDIUM(2) > LOW(1)
        return sorted(tasks, key=lambda t: t._priority.value, reverse=True)

    def get_strategy_name(self) -> str:
        return "PRIORITY"
