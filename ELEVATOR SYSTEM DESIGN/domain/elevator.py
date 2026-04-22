


import uuid

from domain.direction import Direction
from domain.elevator_state import ElevatorState


class Elevator:
    def __init__(self, building_id: str, capacity: int):
        self.id = str(uuid.uuid4())
        self.building_id = building_id
        self.capacity = capacity
        self.current_floor = 1
        self.direction = Direction.IDLE
        self.state = ElevatorState.STOPPED
        self.state_handler = None # Will be set by StoppedState logic


    def is_active(self) -> bool:
        return self.state != ElevatorState.MAINTENANCE

    def is_preparing_for_maintenance(self) -> bool:
        return self.state == ElevatorState.PRE_MAINTENANCE

    def can_accept_external_requests(self) -> bool:
        return self.is_active() and not self.is_preparing_for_maintenance()

    def can_accept_internal_requests(self) -> bool:
        return self.is_active()

    def open_doors(self) -> None:
        print(f"Elevator {self.id} doors opening at floor {self.current_floor}")
        self.state = ElevatorState.DOORS_OPENING

    def close_doors(self) -> None:
        print(f"Elevator {self.id} doors closing")
        self.state = ElevatorState.DOORS_CLOSING

    def enter_maintenance(self) -> None:
        self.close_doors()
        self.state = ElevatorState.MAINTENANCE
        print(f"Elevator {self.id} doors closed, entering maintenance mode")

    def exit_maintenance(self) -> None:
        self.state = ElevatorState.STOPPED
        print(f"Elevator {self.id} exiting maintenance mode and returning to service")
