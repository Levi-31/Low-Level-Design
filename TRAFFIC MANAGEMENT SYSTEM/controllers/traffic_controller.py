from service.traffic_service import TrafficService
from domain.direction import Direction

class TrafficController:
    def __init__(self, traffic_service: TrafficService):
        self.traffic_service = traffic_service
        print("TrafficController initialized")

    def update_vehicle_count(self, direction: Direction, count: int):
        self.traffic_service.update_vehicle_count(direction, count)

    def get_vehicle_count(self, direction: Direction):
        count = self.traffic_service.get_vehicle_count(direction)
        print(f"Traffic count for {direction}: {count}")

    def display_traffic_status(self):
        print("\n--- Traffic Status ---")
        for direction in Direction:
            count = self.traffic_service.get_vehicle_count(direction)
            print(f"  {direction}: {count} vehicles")
        print("----------------------")
