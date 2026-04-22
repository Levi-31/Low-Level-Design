

import uuid

from domain.system_state import SystemState


class Building:
    def __init__(self, name: str, min_floor: int, max_floor: int, total_elevators: int):
        self.id = str(uuid.uuid4())
        self.name = name
        self.min_floor = min_floor
        self.max_floor = max_floor
        self.total_elevators = total_elevators
        self.system_state = SystemState.STOPPED

    def is_valid_floor(self, floor: int) -> bool:
        return self.min_floor <= floor <= self.max_floor