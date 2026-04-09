from typing import Optional
from repository.emergency_repository import EmergencyRepository
from service.intersection_service import IntersectionService
from domain.emergency_request import EmergencyRequest
from domain.direction import Direction

class EmergencyService:
    def __init__(self, emergency_repository: EmergencyRepository, intersection_service: IntersectionService):
        self.emergency_repository = emergency_repository
        self.intersection_service = intersection_service
        print("EmergencyService initialized")

    def request_emergency(self, intersection_id: int, direction: Direction, duration: int):
        if not self.intersection_service.get_intersection(intersection_id):
            print(f"Cannot request emergency: Intersection not found: {intersection_id}")
            return

        request_id = self.emergency_repository.get_next_id()
        request = EmergencyRequest(request_id, intersection_id, direction, duration)
        self.emergency_repository.save(request)

        self.intersection_service.pause_cycle(intersection_id)
        self.intersection_service.emergency_set_all_signals_to_red(intersection_id)
        self.intersection_service.set_signal_to_green(intersection_id, direction)

        intersection = self.intersection_service.get_intersection(intersection_id)
        if intersection:
            intersection.set_emergency_mode(True)
            intersection.set_emergency_direction(direction)

        print(f"Emergency request processed: {request_id} for intersection {intersection_id}, "
              f"direction {direction}, duration {duration}s")

    def end_emergency(self, intersection_id: int):
        active_emergency = self.emergency_repository.get_active_emergency(intersection_id)
        if not active_emergency:
            print(f"No active emergency found for intersection: {intersection_id}")
            return

        self.intersection_service.emergency_set_all_signals_to_red(intersection_id)
        self.emergency_repository.update_status(active_emergency.id, False)

        intersection = self.intersection_service.get_intersection(intersection_id)
        if intersection:
            intersection.set_emergency_mode(False)
            intersection.emergency_direction = None

        self.intersection_service.resume_cycle(intersection_id)
        print(f"Emergency ended for intersection: {intersection_id}")

    def get_active_emergency(self, intersection_id: int) -> Optional[EmergencyRequest]:
        return self.emergency_repository.get_active_emergency(intersection_id)

    def cleanup_expired_emergencies(self):
        self.emergency_repository.remove_expired_requests()
        print("Expired emergency requests cleaned up")
