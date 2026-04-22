


import time
import uuid

from domain.direction import Direction
from domain.request_status import RequestStatus


class ExternalRequest:
    def __init__(self, building_id: str, floor_number: int, direction: Direction):
        self.id = str(uuid.uuid4())
        self.building_id = building_id
        self.floor_number = floor_number
        self.direction = direction
        self.status = RequestStatus.QUEUED
        self.assigned_elevator_id = None
        self.timestamp = time.time()