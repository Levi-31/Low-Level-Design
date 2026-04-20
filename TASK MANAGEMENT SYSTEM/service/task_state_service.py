


from domain.state.cancelled_state import CancelledState
from domain.state.completed_state import CompletedState
from domain.state.in_progress_state import InProgressState
from domain.state.review_state import ReviewState
from domain.state.task_state import TaskState
from domain.state.todo_state import TodoState
from domain.task_status import TaskStatus
from repository.task_repository import TaskRepository


class TaskStateService:
    def __init__(self, task_repository: TaskRepository):
        self._task_repository = task_repository

    def _get_state_instance(self, status: TaskStatus) -> TaskState:
        state_map = {
            TaskStatus.TODO: TodoState,
            TaskStatus.IN_PROGRESS: InProgressState,
            TaskStatus.REVIEW: ReviewState,
            TaskStatus.COMPLETED: CompletedState,
            TaskStatus.CANCELLED: CancelledState,
        }

        if status not in state_map:
            raise Exception("Unknown status")

        return state_map[status]()
    
    def update_task_status(self, task_id: int, new_status: TaskStatus):
        task = self._task_repository.find_by_id(task_id)
        if not task:
            raise Exception("Task not found")

        current_state = self._get_state_instance(task._status)
        current_state.perform_transition(task, new_status)
        self._task_repository.save(task)

    def is_valid_transition(self, current_status: TaskStatus, new_status: TaskStatus) -> bool:
        try:
            state = self._get_state_instance(current_status)
            return state.can_transition_to(new_status)
        except:
            return False