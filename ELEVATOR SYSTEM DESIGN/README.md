# Elevator System Design

This project is a low-level design (LLD) implementation of an Elevator System in Python. It models the core behaviors, components, and strategies required to simulate a scalable multi-elevator system in a building.

## Architecture Flow

The architecture follows a modular, controller-service-repository pattern, segregating responsibilities for better maintainability and scalability.

1. **Controllers (Presentation/Input Layer):**
   - **FloorPanelController:** Handles external requests (users pressing UP/DOWN buttons on a floor).
   - **ElevatorPanelController:** Handles internal requests (users selecting a destination floor inside an elevator).
   - **ElevatorController:** Serves as the primary orchestrator, managing elevator lifecycle (creation, starting, stopping, maintenance).

2. **Services (Business Logic Layer):**
   - **DispatcherService:** Receives external requests and uses a strategy (`ElevatorSelectionStrategy`) to determine the most suitable elevator to dispatch.
   - **ElevatorSchedulerService:** The central engine (or tick runner). In a simulation, it periodically checks and processes queues and elevator movements.
   - **MovementService:** Controls the actual floor-by-floor movement of elevators. It utilizes a `MovementStrategy` (e.g., SCAN, FCFS) to decide the next floor.
   - **RequestService:** Manages the lifecycle of both internal and external requests, updating their states (`PENDING`, `ASSIGNED`, `COMPLETED`).
   - **ElevatorService / BuildingService:** Manages domain entities like `Elevator` and `Building`.

3. **Repositories (Data Access Layer):**
   - In-memory data stores mapping IDs to objects. They provide `save()`, `find_by_id()`, and related query methods for `Building`, `Elevator`, `InternalRequest`, and `ExternalRequest`.

4. **Domain (Core Entities & States):**
   - **Entities:** `Building`, `Elevator`, `InternalRequest`, `ExternalRequest`.
   - **State Pattern:** The elevator uses the State Design Pattern (`ElevatorState`, `ElevatorStateHandler`) to smoothly transition between states (`STOPPED`, `MOVING`, `DOORS_OPENING`, `MAINTENANCE`).
   - **Strategy Pattern:** Uses strategies for movement (`MovementStrategy`) and selection (`ElevatorSelectionStrategy`).

### Request Flow Lifecycle

1. **User requests an elevator:** The `FloorPanelController` creates an `ExternalRequest`.
2. **Dispatching:** The `DispatcherService` queues the request or immediately assigns it to the best available `Elevator` using the selection strategy.
3. **Movement Execution:** The `ElevatorSchedulerService` invokes `MovementService.process_elevator_movement`. The elevator travels towards the target floor.
4. **User boards:** The elevator arrives and opens doors, marking the external request as completed. The user then selects a floor via the `ElevatorPanelController`, creating an `InternalRequest`.
5. **Destination Routing:** The `MovementService` calculates the optimal path using its `MovementStrategy` (e.g., SCAN) to drop off passengers efficiently and securely.

### Sequence Diagram: Handling an External Request

```mermaid
sequenceDiagram
    actor User
    participant FPC as FloorPanelController
    participant RS as RequestService
    participant DS as DispatcherService
    participant MS as MovementService
    participant ESS as ElevatorSchedulerService
    participant Elev as Elevator

    User->>FPC: press_up_button(floor, building_id)
    FPC->>RS: create_external_request()
    RS-->>FPC: ExternalRequest
    FPC->>DS: process_external_request(request)
    DS->>DS: select_best_elevator(request, elevators)
    DS->>RS: assign_request_to_elevator(request.id, elevator.id)
    RS->>RS: create_internal_request(elevator.id, target_floor)

    loop Scheduler Tick
        ESS->>MS: process_elevator_movement(elevator_id)
        MS->>MS: calculate_path(elevator, requests)
        alt Needs to move
            MS->>Elev: Update current_floor, set state to MOVING
        else Reached destination
            MS->>Elev: open_doors()
            MS->>RS: complete_external_request()
            MS->>Elev: close_doors()
        end
    end
```

## UML Class Diagram

```mermaid
classDiagram
    class ElevatorController {
        +create_elevator(building_id: str, capacity: int)
        +move_elevator(elevator_id: str, target_floor: int)
        +set_elevator_maintenance(elevator_id: str, maintenance: bool)
        +start_elevator_system(building_id: str)
        +stop_elevator_system(building_id: str)
    }

    class FloorPanelController {
        +press_up_button(floor_number: int, building_id: str)
        +press_down_button(floor_number: int, building_id: str)
    }

    class ElevatorPanelController {
        +select_floor(elevator_id: str, destination_floor: int)
    }

    class DispatcherService {
        +process_external_request(request: ExternalRequest, building_id: str)
        +assign_request_to_elevator(request: ExternalRequest, elevator: Elevator)
        +process_pending_requests(building_id: str)
    }

    class MovementService {
        +process_all_elevator_movements(building_id: str)
        +process_elevator_movement(elevator_id: str, elevator: Elevator)
    }

    class ElevatorSchedulerService {
        +start_building_scheduler(building_id: str)
        +process_building_operations(building_id: str)
    }

    class Elevator {
        +id: str
        +building_id: str
        +current_floor: int
        +capacity: int
        +direction: Direction
        +state: ElevatorState
        +open_doors()
        +close_doors()
        +enter_maintenance()
        +exit_maintenance()
    }
    
    class Building {
        +id: str
        +name: str
        +min_floor: int
        +max_floor: int
        +total_elevators: int
        +system_state: SystemState
    }

    class ExternalRequest {
        +id: str
        +floor_number: int
        +direction: Direction
        +status: RequestStatus
        +assigned_elevator_id: str
    }

    class InternalRequest {
        +id: str
        +elevator_id: str
        +destination_floor: int
        +status: RequestStatus
    }

    %% Relationships
    ElevatorController --> BuildingService
    ElevatorController --> ElevatorService
    ElevatorController --> RequestService
    ElevatorController --> DispatcherService
    ElevatorController --> MovementService

    FloorPanelController --> ElevatorController
    ElevatorPanelController --> ElevatorController

    DispatcherService --> ElevatorSelectionStrategy
    DispatcherService --> RequestService
    DispatcherService --> ElevatorService

    MovementService --> MovementStrategy
    MovementService --> RequestService
    MovementService --> ElevatorService

    ElevatorSchedulerService --> DispatcherService
    ElevatorSchedulerService --> MovementService

    Elevator --> ElevatorState
    Elevator --> Direction
    ExternalRequest --> Direction
    ExternalRequest --> RequestStatus
    InternalRequest --> RequestStatus

    BuildingService --> BuildingRepository
    ElevatorService --> ElevatorRepository
    RequestService --> ExternalRequestRepository
    RequestService --> InternalRequestRepository
```

## Running the Simulation

Execute the following command to run the predefined simulation ticks in `main.py`:

```bash
python main.py
```
