import sys
import os

from controllers.timing_controller import TimingController
from controllers.traffic_controller import TrafficController

# Add the current directory to sys.path to allow relative imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.emergency_controller import EmergencyController
from controllers.intersection_controller import IntersectionController
from domain.direction import Direction
from repository.intersection_repository import IntersectionRepository
from repository.emergency_repository import EmergencyRepository
from repository.traffic_repository import TrafficRepository
from repository.timing_repository import TimingRepository
from service.intersection_service import IntersectionService
from service.emergency_service import EmergencyService
from service.traffic_service import TrafficService
from service.timing_service import TimingService


def main():
    import pdb;pdb.set_trace()
    print("=== Traffic Signal System Simulation (Python) ===")

    # Initialize repositories
    intersection_repo = IntersectionRepository()
    emergency_repo = EmergencyRepository()
    traffic_repo = TrafficRepository()
    timing_repo = TimingRepository()

    # Initialize services
    intersection_service = IntersectionService(intersection_repo, timing_repo)
    emergency_service = EmergencyService(emergency_repo, intersection_service)
    traffic_service = TrafficService(traffic_repo)
    timing_service = TimingService(timing_repo, traffic_service)

    # Initialize controllers
    intersection_controller = IntersectionController(intersection_service)
    emergency_controller = EmergencyController(emergency_service)
    traffic_controller = TrafficController(traffic_service)
    timing_controller = TimingController(timing_service)

    print("\n--- Creating Intersection ---")
    intersection_controller.create_intersection(1, "Main Street & Oak Avenue")

    print("\n--- Setting Signal Timings ---")
    timing_controller.set_signal_timing(1, Direction.NORTH, 30)
    timing_controller.set_signal_timing(1, Direction.SOUTH, 30)
    timing_controller.set_signal_timing(1, Direction.EAST, 15)
    timing_controller.set_signal_timing(1, Direction.WEST, 15)

    print("\n--- Enabling Dynamic Timing ---")
    timing_controller.enable_dynamic_timing(1, Direction.NORTH, True)
    timing_controller.enable_dynamic_timing(1, Direction.SOUTH, True)

    print("\n--- Starting Automatic Cycle ---")
    intersection_controller.start_cycle(1)

    print("\n--- Displaying Initial Status ---")
    intersection_controller.display_status(1)
    timing_controller.display_timing_status(1)

    print("\n--- Updating Traffic Counts ---")
    traffic_controller.update_vehicle_count(Direction.NORTH, 15)
    traffic_controller.update_vehicle_count(Direction.SOUTH, 8)
    traffic_controller.update_vehicle_count(Direction.EAST, 3)
    traffic_controller.update_vehicle_count(Direction.WEST, 12)

    print("\n--- Displaying Traffic Status ---")
    traffic_controller.display_traffic_status()

    print("\n--- Adjusting Timing Based on Traffic ---")
    timing_controller.adjust_timing_based_on_traffic(1, Direction.NORTH)
    timing_controller.adjust_timing_based_on_traffic(1, Direction.SOUTH)

    print("\n--- Requesting Emergency ---")
    emergency_controller.request_emergency(1, Direction.EAST, 30)

    print("\n--- Displaying Status During Emergency ---")
    intersection_controller.display_status(1)
    emergency_controller.get_emergency_status(1)

    print("\n--- Ending Emergency ---")
    emergency_controller.end_emergency(1)

    print("\n--- Displaying Final Status ---")
    intersection_controller.display_status(1)
    timing_controller.display_timing_status(1)

    print("\n=== Simulation Complete (Python) ===")

if __name__ == "__main__":
    main()
