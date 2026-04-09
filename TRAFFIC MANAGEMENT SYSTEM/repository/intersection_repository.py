from typing import Dict, Optional
from domain.intersection import Intersection
from domain.intersection_cycle import IntersectionCycle
from domain.direction import Direction

class IntersectionRepository:
    def __init__(self):
        self.intersections: Dict[int, Intersection] = {}
        self.cycles: Dict[int, IntersectionCycle] = {}
        self._next_id = 1
        print("IntersectionRepository initialized")

    def save(self, intersection: Intersection):
        self.intersections[intersection.id] = intersection
        print(f"Intersection saved: {intersection.id}")

    def find_by_id(self, intersection_id: int) -> Optional[Intersection]:
        intersection = self.intersections.get(intersection_id)
        if intersection:
            print(f"Intersection found: {intersection_id}")
        else:
            print(f"Intersection not found: {intersection_id}")
        return intersection

    def update_cycle(self, intersection_id: int, cycle: IntersectionCycle):
        self.cycles[intersection_id] = cycle
        print(f"Cycle updated for intersection: {intersection_id}")

    def get_cycle(self, intersection_id: int) -> Optional[IntersectionCycle]:
        cycle = self.cycles.get(intersection_id)
        if cycle:
            print(f"Cycle found for intersection: {intersection_id}")
        else:
            print(f"Cycle not found for intersection: {intersection_id}")
        return cycle

    def update_emergency_mode(self, intersection_id: int, emergency_mode: bool, direction: Direction):
        intersection = self.find_by_id(intersection_id)
        if intersection:
            intersection.set_emergency_mode(emergency_mode)
            intersection.set_emergency_direction(direction)
            print(f"Emergency mode updated for intersection: {intersection_id}")

    def get_next_id(self) -> int:
        id_val = self._next_id
        self._next_id += 1
        return id_val

    def exists(self, intersection_id: int) -> bool:
        return intersection_id in self.intersections
