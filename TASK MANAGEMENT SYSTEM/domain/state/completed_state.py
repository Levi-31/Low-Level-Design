

from domain.state.invalid_state_transition_exception import InvalidStateTransitionException
from domain.state.task_state import TaskState
from domain.task import Task
from domain.task_status import TaskStatus


class CompletedState(TaskState):
    def can_transition_to(self, new_status:TaskStatus):
        return new_status == TaskStatus.IN_PROGRESS
    
    def perform_transition(self,task:Task,new_status:TaskStatus):
        if not self.can_transition_to(new_status):
            if not self.can_transition_to(new_status):
                raise InvalidStateTransitionException(f"Cannot transition from COMPLETED to {new_status.name}")
            task._status = new_status

    def get_state_name(self) -> str:
        return TaskStatus.COMPLETED.value
    