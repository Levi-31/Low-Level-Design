

from datetime import datetime
from typing import List

from domain.task import Task
from domain.task_priority import Priority
from domain.task_search_criteria import TaskSearchCriteria
from repository.task_repository import TaskRepository


class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self._task_repository = task_repository
        self._next_task_id = 1

    def create_task(self, title: str, description: str, due_date: datetime, priority: Priority, creator_id: int) -> Task:
        task = Task(self._next_task_id, title, description, due_date, priority, creator_id)
        self._next_task_id += 1
        return self._task_repository.save(task)
    

    def update_task(self, task_id: int, title: str, description: str, due_date: datetime, priority: Priority) -> Task:
        task = self._task_repository.find_by_id(task_id)
        if not task:
            raise Exception("Task not found")

        task._title = title
        task._description = description
        task._due_date = due_date
        task._priority = priority
        
        task.update_subtask_priorities()
        return self._task_repository.save(task)


    def delete_task(self, task_id: int):
        pass

    def search_tasks(self, criteria: TaskSearchCriteria) -> List[Task]:
        return self._task_repository.search(criteria)
    
    def add_subtask(self, parent_task_id: int, title: str, description: str, due_date: datetime, priority: Priority, creator_id: int) -> Task:
        parent_task = self._task_repository.find_by_id(parent_task_id)
        if not parent_task:
            raise Exception("Parent task not found")

        subtask = Task(self._next_task_id, title, description, due_date, priority, creator_id, parent_task_id)
        self._next_task_id += 1
        
        parent_task.add_subtask(subtask)
        self._task_repository.save(subtask)
        self._task_repository.save(parent_task)
        return subtask