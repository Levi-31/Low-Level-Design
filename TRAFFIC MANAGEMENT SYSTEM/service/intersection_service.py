from typing import Optional

from domain.direction import Direction
from domain.intersection import Intersection
from domain.intersection_cycle import IntersectionCycle
from repository.intersection_repository import IntersectionRepository
from repository.timing_repository import TimingRepository


class IntersectionService:
    def __init__(self, intersection_repository:IntersectionRepository,timing_repository:TimingRepository):
        self.intersection_repository = intersection_repository
        self.timing_repository = timing_repository

    def create_intersection(self,id:int, name:str):
        if self.intersection_repository.exists(id):
            print(f"Intersection with ID {id} already exists")
            return
        
        intersection = Intersection(id,name)
        self.intersection_repository.save(intersection)
        self.timing_repository.initialize_default_timings(id)

        cycle = IntersectionCycle(id)
        self.intersection_repository.update_cycle(id, cycle)

        self.start_automatic_cycle(id)
        print(f"Intersection created successfully: {name} (ID: {id})")


    def get_intersection(self, intersection_id: int) -> Optional[Intersection]:
        return self.intersection_repository.find_by_id(intersection_id)
    
    def start_automatic_cycle(self, intersection_id: int):
        intersection = self.intersection_repository.find_by_id(intersection_id)
        if not intersection:
            return

        cycle = self.intersection_repository.get_cycle(intersection_id)
        if not cycle:
            cycle = IntersectionCycle(intersection_id)
            self.intersection_repository.update_cycle(intersection_id, cycle)

        cycle.set_paused(False)
        intersection.set_cycle_paused(False)
        print(f"Automatic cycle started for intersection: {intersection_id}")
        print("TODO: Implement timer-based automatic cycling")

    def pause_cycle(self, intersection_id: int):
        intersection = self.intersection_repository.find_by_id(intersection_id)
        if not intersection:
            return

        cycle = self.intersection_repository.get_cycle(intersection_id)
        if cycle:
            cycle.set_paused(True)
            intersection.set_cycle_paused(True)
            print(f"Cycle paused for intersection: {intersection_id}")

    
    def resume_cycle(self, intersection_id: int):
        intersection = self.intersection_repository.find_by_id(intersection_id)
        if not intersection:
            return

        cycle = self.intersection_repository.get_cycle(intersection_id)
        if cycle:
            cycle.set_paused(False)
            intersection.set_cycle_paused(False)
            print(f"Cycle resumed for intersection: {intersection_id}")

    def get_cycle(self, intersection_id: int) -> Optional[IntersectionCycle]:
        return self.intersection_repository.get_cycle(intersection_id)

    def set_all_signals_to_red(self, intersection_id: int):
        intersection = self.intersection_repository.find_by_id(intersection_id)
        if intersection:
            intersection.set_all_signals_to_red()

    def emergency_set_all_signals_to_red(self, intersection_id: int):
        intersection = self.intersection_repository.find_by_id(intersection_id)
        if intersection:
            for direction in Direction:
                intersection.emergency_transition_to_red(direction)
            print(f"Emergency: All signals transitioned to RED for intersection {intersection_id}")

    def set_signal_to_green(self, intersection_id: int, direction: Direction):
        intersection = self.intersection_repository.find_by_id(intersection_id)
        if intersection:
            intersection.set_signal_to_green(direction)

    def set_signal_to_yellow(self, intersection_id: int, direction: Direction):
        intersection = self.intersection_repository.find_by_id(intersection_id)
        if intersection:
            intersection.set_signal_to_yellow(direction)

    def set_signal_to_red(self, intersection_id: int, direction: Direction):
        intersection = self.intersection_repository.find_by_id(intersection_id)
        if intersection:
            intersection.set_signal_to_red(direction)

    def set_signal_to_off(self, intersection_id: int, direction: Direction):
        intersection = self.intersection_repository.find_by_id(intersection_id)
        if intersection:
            intersection.set_signal_to_off(direction)

    def get_paused_phase(self, intersection_id: int) -> int:
        cycle = self.intersection_repository.get_cycle(intersection_id)
        return cycle.paused_at_phase if cycle else 0
