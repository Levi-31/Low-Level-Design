from typing import Dict, Optional
from domain.emergency_request import EmergencyRequest

class EmergencyRepository:
    def __init__(self):
        self.requests: Dict[int, EmergencyRequest] = {}
        self._next_id = 1

    def save(self, request: EmergencyRequest):
        self.requests[request.id] = request
        print(f"Emergency request saved: {request.id}")

    def get_active_emergency(self, intersection_id: int) -> Optional[EmergencyRequest]:
        for request in self.requests.values():
            if request.intersection_id == intersection_id and request.is_active:
                return request
        return None

    def update_status(self, request_id: int, is_active: bool):
        request = self.requests.get(request_id)
        if request:
            request.set_active(is_active)

    def remove_expired_requests(self):
        to_remove = [rid for rid, req in self.requests.items() if req.is_expired()]
        for rid in to_remove:
            del self.requests[rid]

    def get_next_id(self) -> int:
        id_val = self._next_id
        self._next_id += 1
        return id_val
