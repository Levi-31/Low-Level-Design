from typing import Dict
from domain.direction import Direction
from domain.vehicle_counter import VehicleCounter

class TrafficRepository:
    def __init__(self):
        self.counters: Dict[Direction, VehicleCounter] = {
            dir: VehicleCounter(dir) for dir in Direction
        }

    def update_count(self, direction: Direction, count: int):
        counter = self.counters.get(direction)
        if counter:
            counter.update_count(count)

    def get_count(self, direction: Direction) -> int:
        counter = self.counters.get(direction)
        return counter.count if counter else 0

    def reset_all(self):
        for counter in self.counters.values():
            counter.reset_count()
