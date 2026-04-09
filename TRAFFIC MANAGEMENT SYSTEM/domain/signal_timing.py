
from typing import List

from domain.direction import Direction

class SignalTiming:
    YELLOW_DURATION = 3 # constant 

    def __init__(self, intersection_id: int, direction: Direction):
        self.intersection_id = intersection_id
        self.direction = direction
        self.green_duration = 45
        self.is_dynamic = False
        print(f"Signal timing created for intersection {intersection_id}, direction {direction}")

    def set_green_duration(self, green_duration: int):
        self.green_duration = green_duration
        print(f"Green duration set to {green_duration} seconds for {self.direction}")

    def set_dynamic(self, dynamic: bool):
        self.is_dynamic = dynamic
        print(f"Dynamic timing {'enabled' if dynamic else 'disabled'} for {self.direction}")

    def update_timing(self, green_duration: int):
        self.green_duration = green_duration
        print(f"Timing updated for {self.direction}: Y={self.YELLOW_DURATION}s, G={green_duration}s")

    def calculate_red_duration(self, all_timings: List['SignalTiming']) -> int:
        red_duration = 0
        for timing in all_timings:
            if timing.direction != self.direction:
                red_duration += timing.green_duration + self.YELLOW_DURATION
        return red_duration

    def get_total_cycle_time(self, all_timings: List['SignalTiming']) -> int:
        return self.green_duration + self.YELLOW_DURATION + self.calculate_red_duration(all_timings)

    def __str__(self):
        return f"SignalTiming{{intersection_id={self.intersection_id}, direction={self.direction}, yellow_duration={self.YELLOW_DURATION}, green_duration={self.green_duration}, is_dynamic={self.is_dynamic}}}"
