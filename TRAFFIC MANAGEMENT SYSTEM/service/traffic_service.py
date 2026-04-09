from repository.traffic_repository import TrafficRepository
from domain.direction import Direction

class TrafficService:
    def __init__(self, traffic_repository: TrafficRepository):
        self.traffic_repository = traffic_repository
        print("TrafficService initialized")

    def update_vehicle_count(self, direction: Direction, count: int):
        self.traffic_repository.update_count(direction, count)
        print(f"Vehicle count updated: {direction} = {count}")

    def get_vehicle_count(self, direction: Direction) -> int:
        return self.traffic_repository.get_count(direction)
