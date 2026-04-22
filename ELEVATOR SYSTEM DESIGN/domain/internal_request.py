



import time
import uuid

from domain.request_status import RequestStatus


class InternalRequest:
    def __init__(self, elevator_id: str, destination_floor: int):
        self.id = str(uuid.uuid4())
        self.elevator_id = elevator_id
        self.destination_floor = destination_floor
        self.status = RequestStatus.PENDING
        self.timestamp = time.time()