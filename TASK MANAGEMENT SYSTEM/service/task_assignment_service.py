


from domain.change_type import ChangeType
from repository.task_repository import TaskRepository
from repository.user_repository import UserRepository


class TaskAssignmentService:
    def __init__(self, task_repository: TaskRepository, user_repository: UserRepository):
        self._task_repository = task_repository
        self._user_repository = user_repository

    
    def assign_task(self, task_id: int, assignee_id: int):
        task = self._task_repository.find_by_id(task_id)
        if not task:
            raise Exception("Task not found")

        user = self._user_repository.find_by_id(assignee_id)
        if not user:
            raise Exception("Assignee User not found")

        old_assignee = str(task._assignee_id)
        task._assignee_id = assignee_id
        
        task.notify_subscribers(ChangeType.ASSIGNED, old_assignee, str(assignee_id))
        self._task_repository.save(task)