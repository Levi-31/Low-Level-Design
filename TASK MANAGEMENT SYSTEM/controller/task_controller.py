



from datetime import datetime
from typing import List

from domain.task import Task
from domain.task_priority import Priority
from domain.task_search_criteria import TaskSearchCriteria
from service.task_service import TaskService


class TaskController:
    def __init__(self, task_service: TaskService):
        self._task_service = task_service

    def _parse_priority(self, priority_str: str) -> Priority:
        priority_map = {
            "URGENT": Priority.URGENT,
            "HIGH": Priority.HIGH,
            "MEDIUM": Priority.MEDIUM,
            "LOW": Priority.LOW,
        }
    
        return priority_map.get(priority_str.upper(), Priority.LOW)

    def create_task(self, title: str, description: str, due_date: datetime, priority_str: str, creator_id: int) -> Task:
        return self._task_service.create_task(title, description, due_date, self._parse_priority(priority_str), creator_id)

    def update_task(self, task_id: int, title: str, description: str, due_date: datetime, priority_str: str) -> Task:
        return self._task_service.update_task(task_id, title, description, due_date, self._parse_priority(priority_str))

    def delete_task(self, task_id: int):
        self._task_service.delete_task(task_id)

    def search_tasks(self, criteria: TaskSearchCriteria) -> List[Task]:
        return self._task_service.search_tasks(criteria)

    def add_subtask(self, parent_task_id: int, title: str, description: str, due_date: datetime, priority_str: str, creator_id: int) -> Task:
        return self._task_service.add_subtask(parent_task_id, title, description, due_date, self._parse_priority(priority_str), creator_id)
