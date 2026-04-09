from service.timing_service import TimingService
from domain.direction import Direction

class TimingController:
    def __init__(self, timing_service: TimingService):
        self.timing_service = timing_service
        print("TimingController initialized")

    def set_signal_timing(self, intersection_id: int, direction: Direction, green_duration: int):
        self.timing_service.set_signal_timing(intersection_id, direction, green_duration)

    def enable_dynamic_timing(self, intersection_id: int, direction: Direction, enable: bool):
        self.timing_service.enable_dynamic_timing(intersection_id, direction, enable)

    def get_signal_timing(self, intersection_id: int, direction: Direction):
        timing = self.timing_service.get_signal_timing(intersection_id, direction)
        if timing:
            print(f"Signal timing for {direction}: {timing}")

    def adjust_timing_based_on_traffic(self, intersection_id: int, direction: Direction):
        self.timing_service.adjust_timing_based_on_traffic(intersection_id, direction)

    def display_timing_status(self, intersection_id: int):
        print(f"\n--- Timing Status: {intersection_id} ---")
        for direction in Direction:
            timing = self.timing_service.get_signal_timing(intersection_id, direction)
            if timing:
                print(f"  {timing}")
        print("------------------------------------------")
