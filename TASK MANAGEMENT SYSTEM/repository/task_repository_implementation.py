

from typing import Dict, List, Optional

from domain.strategy.created_date_sorting import CreatedDateSortingStrategy
from domain.strategy.due_date_sorting import DueDateSortingStrategy
from domain.strategy.priority_sorting import PrioritySortingStrategy
from domain.strategy.task_sorting_context import TaskSortingContext
from domain.task import Task
from domain.task_search_criteria import TaskSearchCriteria
from repository.task_repository import TaskRepository


class TaskRepositoryImpl(TaskRepository):
    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id = 1


    def save(self,task:Task):
        if task._id >= self._next_id:
            self._next_id = task._id + 1
        self._tasks[task._id] = task
        return task
    

    def find_by_id(self, task_id: int) -> Optional[Task]:
        return self._tasks.get(task_id)
    
    def find_by_assignee(self, assignee_id: int) -> List[Task]:
        return [t for t in self._tasks.values() if t._assignee_id == assignee_id]
    
    def find_by_parent_task(self, parent_task_id: int) -> List[Task]:
        return [t for t in self._tasks.values() if t._parent_task_id == parent_task_id]
    
    def search(self, criteria: TaskSearchCriteria) -> List[Task]:
        filtered = []
        for task in self._tasks.values():
            matches = True
            
            if criteria.get_assignee_id is not None and task._assignee_id != criteria.get_assignee_id:
                matches = False
            if criteria.get_creator_id is not None and task._creator_id != criteria.get_creator_id:
                matches = False
            if criteria.get_priority is not None and task._priority != criteria.get_priority:
                matches = False
            if criteria.get_status is not None and task._status != criteria.get_status:
                matches = False
            if criteria.get_has_subtasks is not None and task.has_subtasks() != criteria.get_has_subtasks:
                matches = False
                
            if matches:
                filtered.append(task)
                
        context = TaskSortingContext()
        if criteria.get_sort_by == "due_date" or criteria.get_sort_by == "dueDate":
            context.set_sorting_strategy(DueDateSortingStrategy())
        elif criteria.get_sort_by == "created_date" or criteria.get_sort_by == "createdDate":
            context.set_sorting_strategy(CreatedDateSortingStrategy())
        else:
            context.set_sorting_strategy(PrioritySortingStrategy())
            
        sorted_tasks = context.sort_tasks(filtered)

        # Strategies sort descending conceptually or uniquely. Reverse if needed.
        # Priority and CreatedDate usually sort descending by default. DueDate sorts ascending by default.
        is_due_date = "due" in criteria.get_sort_by.lower()
        if criteria.get_sort_order == "asc" and not is_due_date:
            sorted_tasks.reverse()
        elif criteria.get_sort_order == "desc" and is_due_date:
            sorted_tasks.reverse()
            
        return sorted_tasks