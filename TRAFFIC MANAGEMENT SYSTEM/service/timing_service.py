from typing import Optional
from repository.timing_repository import TimingRepository
from service.traffic_service import TrafficService
from domain.direction import Direction
from domain.signal_timing import SignalTiming

class TimingService:
    def __init__(self, timing_repository: TimingRepository, traffic_service: TrafficService):
        self.timing_repository = timing_repository
        self.traffic_service = traffic_service
        print("TimingService initialized")

    def set_signal_timing(self, intersection_id: int, direction: Direction, green_duration: int):
        self.timing_repository.update_signal_timing(intersection_id, direction, green_duration)
        print(f"Signal timing set: {direction} = {green_duration}s")

    def enable_dynamic_timing(self, intersection_id: int, direction: Direction, enable: bool):
        timing = self.timing_repository.get_signal_timing(intersection_id, direction)
        if timing:
            timing.set_dynamic(enable)
            print(f"Dynamic timing {'enabled' if enable else 'disabled'} for {direction}")

    def get_signal_timing(self, intersection_id: int, direction: Direction) -> Optional[SignalTiming]:
        return self.timing_repository.get_signal_timing(intersection_id, direction)

    def adjust_timing_based_on_traffic(self, intersection_id: int, direction: Direction):
        timing = self.timing_repository.get_signal_timing(intersection_id, direction)
        if timing and timing.is_dynamic:
            count = self.traffic_service.get_vehicle_count(direction)
            new_duration = self.calculate_optimal_green_duration(count)
            timing.update_timing(new_duration)
            print(f"Adjusted timing for {direction} to {new_duration}s based on traffic ({count})")

    def calculate_optimal_green_duration(self, vehicle_count: int) -> int:
        # Basic logic: base 20s + 2s per vehicle, max 60s
        return min(60, 20 + (vehicle_count * 2))
