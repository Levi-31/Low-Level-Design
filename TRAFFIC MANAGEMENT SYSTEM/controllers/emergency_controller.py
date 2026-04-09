from service.emergency_service import EmergencyService
from domain.direction import Direction

class EmergencyController:
    def __init__(self, emergency_service: EmergencyService):
        self.emergency_service = emergency_service
        print("EmergencyController initialized")

    def request_emergency(self, intersection_id: int, direction: Direction, duration: int):
        self.emergency_service.request_emergency(intersection_id, direction, duration)

    def end_emergency(self, intersection_id: int):
        self.emergency_service.end_emergency(intersection_id)

    def get_emergency_status(self, intersection_id: int):
        request = self.emergency_service.get_active_emergency(intersection_id)
        if request:
            print(f"\n--- Emergency Status: {intersection_id} ---")
            print(request)
            print("------------------------------------------")
        else:
            print(f"No active emergency for intersection {intersection_id}")
