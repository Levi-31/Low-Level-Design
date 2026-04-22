from typing import TYPE_CHECKING, Any
from domain.state.elevator_state_handler import ElevatorStateHandler
from domain.elevator_state import ElevatorState

if TYPE_CHECKING:
    from domain.elevator import Elevator

class StoppedState(ElevatorStateHandler):
    def handle_request(self, elevator: 'Elevator', request: Any) -> None:
        pass

    def update_state(self, elevator: 'Elevator') -> None:
        pass

    def get_state_name(self) -> str:
        return ElevatorState.STOPPED.value

class MovingState(ElevatorStateHandler):
    def handle_request(self, elevator: 'Elevator', request: Any) -> None:
        pass

    def update_state(self, elevator: 'Elevator') -> None:
        pass

    def get_state_name(self) -> str:
        return ElevatorState.MOVING.value

class DoorsOpeningState(ElevatorStateHandler):
    def handle_request(self, elevator: 'Elevator', request: Any) -> None:
        pass

    def update_state(self, elevator: 'Elevator') -> None:
        pass

    def get_state_name(self) -> str:
        return ElevatorState.DOORS_OPENING.value

class DoorsClosingState(ElevatorStateHandler):
    def handle_request(self, elevator: 'Elevator', request: Any) -> None:
        pass

    def update_state(self, elevator: 'Elevator') -> None:
        pass

    def get_state_name(self) -> str:
        return ElevatorState.DOORS_CLOSING.value

class MaintenanceState(ElevatorStateHandler):
    def handle_request(self, elevator: 'Elevator', request: Any) -> None:
        pass

    def update_state(self, elevator: 'Elevator') -> None:
        pass

    def get_state_name(self) -> str:
        return ElevatorState.MAINTENANCE.value

class PreMaintenanceState(ElevatorStateHandler):
    def handle_request(self, elevator: 'Elevator', request: Any) -> None:
        pass

    def update_state(self, elevator: 'Elevator') -> None:
        pass

    def get_state_name(self) -> str:
        return ElevatorState.PRE_MAINTENANCE.value
