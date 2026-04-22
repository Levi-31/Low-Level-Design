


from controller.elevator_controller import ElevatorController
from domain.direction import Direction


class FloorPanelController:
    def __init__(self, elevator_controller: ElevatorController) -> None:
        self.request_service = elevator_controller.request_service
        self.building_service = elevator_controller.building_service
        self.dispatcher_service = elevator_controller.dispatcher_service

    def press_up_button(self, floor_number: int, building_id: str) -> None:
        if not self.building_service.is_valid_floor(building_id, floor_number):
            raise ValueError(f"Invalid floor number: {floor_number}")

        if not self.building_service.is_system_running(building_id):
            print("Elevator system is not running. Request rejected.")
            return

        request = self.request_service.create_external_request(floor_number, Direction.UP, building_id)
        self.dispatcher_service.process_external_request(request, building_id)
        print(f"UP button pressed on floor {floor_number}")


    def press_down_button(self, floor_number: int, building_id: str) -> None:
        if not self.building_service.is_valid_floor(building_id, floor_number):
            raise ValueError(f"Invalid floor number: {floor_number}")

        if not self.building_service.is_system_running(building_id):
            print("Elevator system is not running. Request rejected.")
            return

        request = self.request_service.create_external_request(floor_number, Direction.DOWN, building_id)
        self.dispatcher_service.process_external_request(request, building_id)
        print(f"DOWN button pressed on floor {floor_number}")
