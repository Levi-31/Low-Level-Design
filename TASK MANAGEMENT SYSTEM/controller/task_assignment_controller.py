


from service.task_assignment_service import TaskAssignmentService


class TaskAssignmentController:
    def __init__(self, task_assignment_service: TaskAssignmentService):
        self._task_assignment_service = task_assignment_service

    def assign_task(self, task_id: int, assignee_id: int):
        self._task_assignment_service.assign_task(task_id, assignee_id)