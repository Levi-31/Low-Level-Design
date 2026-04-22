

from controller.elevator_controller import ElevatorController


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controller.elevator_controller import ElevatorController

class ElevatorPanelController:
    def __init__(self, elevator_controller: 'ElevatorController') -> None:
        self.request_service = elevator_controller.request_service
        self.elevator_service = elevator_controller.elevator_service
        self.building_service = elevator_controller.building_service

    def select_floor(self, elevator_id: str, destination_floor: int) -> None:
        elevator = self.elevator_service.find_by_id(elevator_id)
        if not elevator:
            raise ValueError(f"Elevator not found: {elevator_id}")

        if not self.building_service.is_valid_floor(elevator.building_id, destination_floor):
            raise ValueError(f"Invalid floor number: {destination_floor}")

        if elevator.current_floor == destination_floor:
            print(f"Elevator is already on floor {destination_floor}")
            return

        if not elevator.can_accept_internal_requests():
            print(f"Elevator {elevator_id} cannot accept new requests in current state")
            return

        self.request_service.create_internal_request(elevator_id, destination_floor)
        print(f"Floor {destination_floor} selected in elevator {elevator_id}")
