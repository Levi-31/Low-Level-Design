


import time

from controller.elevator_controller import ElevatorController
from controller.elevator_panel_controller import ElevatorPanelController
from controller.floor_panel_controller import FloorPanelController
from service.elevator_schedule_service import ElevatorSchedulerService


def run_simulation() -> None:
    # Initialize Controllers
    elevator_controller = ElevatorController()
    elevator_panel_controller = ElevatorPanelController(elevator_controller)
    floor_panel_controller = FloorPanelController(elevator_controller)

    # Initialize Scheduler
    scheduler_service = ElevatorSchedulerService(
        elevator_controller.elevator_service,
        elevator_controller.request_service,
        elevator_controller.movement_service,
        elevator_controller.dispatcher_service
    )

    # 1. Setup Building and Elevators
    building = elevator_controller.building_service.create_building("Global Trade Center", 1, 10, 3)
    building_id = building.id
    
    e1 = elevator_controller.create_elevator(building_id, 10)
    e2 = elevator_controller.create_elevator(building_id, 10)
    e3 = elevator_controller.create_elevator(building_id, 10)

    
    print("--- Initialized Building with 3 Elevators ---")
    print(f"Elevator 1 ID: {e1.id}")
    print(f"Elevator 2 ID: {e2.id}")
    print(f"Elevator 3 ID: {e3.id}")

    # 2. Start the system
    elevator_controller.start_elevator_system(building_id)
    scheduler_service.start_building_scheduler(building_id)

    # 3. Simulate external requests
    print("\n--- Simulating External Requests ---")
    floor_panel_controller.press_up_button(1, building_id)
    floor_panel_controller.press_up_button(3, building_id)
    floor_panel_controller.press_down_button(7, building_id)

    # Run simulation ticks
    for i in range(5):
        print(f"\n--- Simulation Tick {i + 1} ---")
        scheduler_service.process_building_operations(building_id)
        time.sleep(0.1)

    # 4. Simulate internal requests
    print("\n--- Simulating Internal Requests ---")
    elevator_panel_controller.select_floor(e1.id, 5)
    elevator_panel_controller.select_floor(e2.id, 8)

    for i in range(10):
        print(f"\n--- Simulation Tick {i + 6} ---")
        scheduler_service.process_building_operations(building_id)
        time.sleep(0.1)

    # 5. Maintenance Mode Test
    print("\n--- Testing Maintenance Mode ---")
    elevator_controller.set_elevator_maintenance(e1.id, True)

    floor_panel_controller.press_up_button(4, building_id)

    for i in range(5):
        print(f"\n--- Simulation Tick {i + 16} ---")
        scheduler_service.process_building_operations(building_id)
        time.sleep(0.1)

    elevator_controller.set_elevator_maintenance(e1.id, False)

    print("\n--- Final Simulation ticks ---")
    for i in range(5):
        scheduler_service.process_building_operations(building_id)
        time.sleep(0.1)

    # Stop system
    scheduler_service.stop_building_scheduler(building_id)
    elevator_controller.stop_elevator_system(building_id)

if __name__ == "__main__":
    try:
        run_simulation()
    except Exception as e:
        print(f"Simulation failed: {e}")
