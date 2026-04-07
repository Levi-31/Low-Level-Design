# Parking Lot Design Documentation

## 1. Introduction
This documentation provides a comprehensive overview of the Low-Level Design (LLD) for the modular Parking Lot System implemented in Python. The system follows Domain-Driven Design (DDD) principles and an underlying Clean Architecture (Controller &rarr; Service &rarr; Repository &rarr; Domain).

## 2. Architecture Overview
- **Domain**: Contains the core business entities (`Vehicle`, `Ticket`, `Receipt`, `Payment`, `ParkingSlot`, `Floor`, `PricingRule`).
- **Repository**: Handles data storage abstraction (currently utilizing in-memory structures for simulation) mapping to `FloorRepository`, `SlotRepository`, `TicketRepository`, etc.
- **Service**: Encapsulates specific business logic operations and coordinates operations between disparate domains and repositories (`AdminService`, `TicketService`, `PricingService`, `PaymentService`, etc.).
- **Adapter**: Provides standardized interfaces integrating external dependency endpoints like mock payment gateways (`RazorpayAdapter`, `StripeAdapter`).
- **Controller**: Acts as the simulation entry junction exposing methods for end-user and administrative requests (`AdminController`, `EntryController`, `ExitController`).

## 3. Flow & Architecture Diagrams (UML)

The following UML Class Diagram details all active classes, their attributes, core methods, and relationships mapping out how the modular subsystems tie together.

### 3.1 Domain & Service Layer Class Diagram
```mermaid
classDiagram

class VehicleType {
    <<enumeration>>
    BIKE
    CAR
    TRUCK
    EV
}

class Vehicle {
    +UUID id
    +String vehicle_number
    +VehicleType vehicle_type
}

class ParkingSlot {
    +UUID id
    +VehicleType slot_type
    +int floor_number
    +bool is_occupied
}

class Floor {
    +UUID id
    +int floor_number
    +List~ParkingSlot~ slots
    +add_slots(ParkingSlot)
    +get_available_parking_slot(VehicleType) List~ParkingSlot~
    +get_available_slot_count(VehicleType) int
}

class Ticket {
    +UUID id
    +String vehicle_id
    +String slot_id
    +datetime entry_time
    +bool is_active
    +deactivate()
}

class Receipt {
    +UUID id
    +String ticket_id
    +datetime exit_time
    +float total_fees
    +PaymentStatus payment_status
    +mark_as_paid()
}

class Payment {
    +UUID id
    +String ticket_id
    +float amount
    +PaymentGateway gateway
    +PaymentStatus status
    +mark_as_success()
    +mark_as_failed()
}

class PricingRule {
    +UUID id
    +VehicleType vehicle_type
    +float rate_per_hour
    +float flat_rate
    +update_rates(rate_per_hour, flat_rate)
}

class EntryController {
    +enter_vehicle(license_plate, vehicle_type) EntryResult
}

class ExitController {
    +exit_vehicle(ticket_id) ExitResult
    +generate_receipt_text(ticket_id) String
}

class AdminController {
    +initialize_parking_lot()
    +add_floor(floor_number)
    +add_slots_to_floor(floor_number, slot_type, count)
    +update_pricing_rule(vehicle_type, rate_per_hour, flat_rate)
    +get_parking_status() dict
}

class AdminService {
    +initialize_parking_lot()
    +add_floor_public(floor_number)
    +add_slots_to_floor_public(floor_number, slot_type, count)
    +update_pricing_rule(vehicle_type, rate, flat)
    +get_parking_status()
}

class TicketService {
    +generate_ticket(vehicle, slot_id) Ticket
    +get_ticket(ticket_id) Ticket
    +deactivate_ticket(ticket_id)
}

class SlotService {
    +allocate_slot(vehicle_type) ParkingSlot
    +release_slot(slot_id)
    +create_slot(slot_type, floor_number) ParkingSlot
    +get_available_slot_count(vehicle_type) int
}

class PricingService {
    +calculate_fee(ticket) float
}

class PaymentService {
    +process_payment(ticket_id, amount) bool
    +process_payment_with_retry(ticket_id, amount, max_retries) bool
}


Vehicle "1" -- "1" VehicleType
Floor "1" *-- "many" ParkingSlot
ParkingSlot "*" -- "1" VehicleType
Ticket "1" -- "1" Vehicle
Ticket "1" -- "1" ParkingSlot
Receipt "1" -- "1" Ticket
Payment "1" -- "1" Ticket
PricingRule "1" -- "1" VehicleType

EntryController --> TicketService
EntryController --> SlotService
ExitController --> TicketService
ExitController --> PricingService
ExitController --> PaymentService
ExitController --> SlotService
AdminController --> AdminService

AdminService --> Floor
AdminService --> ParkingSlot
AdminService --> PricingRule
```

## 4. System Design Patterns Utilized
1.  **Repository Pattern**: Isolates data access operations. The abstraction ensures that if this system scales to employ a proper SQL or NoSQL database, the overall service layer won't require restructuring.
2.  **Strategy / Adapter Pattern**: Coordinates multiple mocked external payment gateways cleanly. The base abstract implementations allow expanding into additional processors with ease.
3.  **Dependency Injection**: Controllers consistently acquire instances of required `Services` explicitly via class constructors. Rather than locally instantiating dependencies, components expect the dependency context. Noticeable in `main()` injection wiring schemas.
4.  **MVC & Service-layer separation**: A strict separation isolating entry endpoints (controllers), operational business processes (services), and localized data stores (repositories).

## 5. Summary of Operations
- **System Bootstrapping**: Handled by the `AdminController` which establishes structural objects (Floors, respective multi-tiered Slots) alongside generic Pricing structures.
- **Entering the System**: Exclusively searches for correctly sized spatial allocations via resolving through the `SlotService`. The creation of a unified `Ticket` bridges a `Vehicle` with structural tracking endpoints and anchors exact entrance temporal markers.
- **Exiting workflows**: Heavily leverages `PricingService` heuristics (accounting for generic per-hour models intersecting flat rates alongside specific class limitations). Introduces an autonomous fallback mechanic resolving monetary actions iteratively in the `PaymentService` utilizing independent adapter systems prior to printing consolidated standard receipts.
