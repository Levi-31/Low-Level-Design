

from domain.state.invalid_state_transition_exception import InvalidStateTransitionException
from domain.state.task_state import TaskState
from domain.task import Task
from domain.task_status import TaskStatus


class CancelledState(TaskState):
    def can_transition_to(self, new_status: TaskStatus) -> bool:
        return new_status in [TaskStatus.TODO]

    def perform_transition(self, task: Task, new_status: TaskStatus):
        if not self.can_transition_to(new_status):
            raise InvalidStateTransitionException(f"Cannot transition from CANCELLED to {new_status.name}")
        task._status = new_status

    def get_state_name(self) -> str:
        return TaskStatus.CANCELLED.value
