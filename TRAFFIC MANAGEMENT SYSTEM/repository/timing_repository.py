from typing import Dict, List, Optional
from domain.direction import Direction
from domain.signal_timing import SignalTiming

class TimingRepository:
    def __init__(self):
        # Key: intersection_id -> (Map: Direction -> SignalTiming)
        self.timings: Dict[int, Dict[Direction, SignalTiming]] = {}

    def save_signal_timing(self, timing: SignalTiming):
        if timing.intersection_id not in self.timings:
            self.timings[timing.intersection_id] = {}
        self.timings[timing.intersection_id][timing.direction] = timing
        print(f"Signal timing saved for intersection {timing.intersection_id}, direction {timing.direction}")

    def get_signal_timing(self, intersection_id: int, direction: Direction) -> Optional[SignalTiming]:
        return self.timings.get(intersection_id, {}).get(direction)

    def update_signal_timing(self, intersection_id: int, direction: Direction, green_duration: int):
        timing = self.get_signal_timing(intersection_id, direction)
        if timing:
            timing.set_green_duration(green_duration)

    def initialize_default_timings(self, intersection_id: int):
        for direction in Direction:
            self.save_signal_timing(SignalTiming(intersection_id, direction))
        print(f"Default timings initialized for intersection {intersection_id}")

    def get_all_timings_for_intersection(self, intersection_id: int) -> List[SignalTiming]:
        return list(self.timings.get(intersection_id, {}).values())
