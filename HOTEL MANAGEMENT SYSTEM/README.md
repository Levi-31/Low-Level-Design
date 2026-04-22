# Hotel Management System

A robust, low-level design (LLD) implementation of a Hotel Management System in Python. This project follows a structured, multi-layer architecture incorporating Controllers, Services, Repositories, and Domain Models to provide a clean separation of concerns and scalable business logic.

## Architecture & System Design

The system is designed with Domain-Driven Design (DDD) principles in a layered architecture:

- **Domain Layer**: Contains the core business entities (Models/Data Classes) such as `Hotel`, `Room`, `RoomType`, `User`, `Booking`, `Transaction`, and various policy models.
- **Repository Layer**: Handles data persistence. It abstracts database interactions using interfaces and implementations (e.g., `HotelRepositoryImpl`, `BookingRepositoryImpl`), allowing mock implementations or easy swapping of database providers without impacting other system layers.
- **Service Layer**: Contains the core business logic. It orchestrates interactions between repositories and external services (e.g., `BookingService`, `PricingService`, `InventoryService`, `SearchService`).
- **Controller Layer**: Exposes endpoints and orchestrates the flow of data between the user interfaces (or API routes) and the business services (e.g., `AdminController`, `SearchController`, `BookingController`).

## Key Features

- **Inventory Management**: Track and manage hotels, room types, and specific room availability. Handles overbooking policies and capacity management.
- **Dynamic Pricing**: Configure base prices and seasonal pricing overrides for specific dates and room types.
- **Search & Availability**: Search for available rooms across date ranges with built-in availability calculations.
- **Booking Lifecycle**: Seamlessly handle booking creation, confirmation via transactions, check-in, check-out, and transparent cancellation policies.
- **Transaction & Payment Handling**: Mock transaction integrations supporting pending, completed, and failed states to confirm reservations.
- **Roles & User Management**: Different access patterns like customer dashboard and admin management workflows.

## Class Diagram (UML)

```mermaid
classDiagram
    %% Controllers
    class AdminController {
        -hotel_repository
        -room_type_repository
        -room_repository
        -seasonal_price_repository
        -cancellation_policy_repository
        -booking_service
        +create_or_update_policy(policy)
        +create_or_update_hotel(hotel)
        +create_or_update_room_type(room_type)
        +set_seasonal_price(...)
        +check_in(...)
        +check_out(...)
    }
    
    class BookingController {
        -booking_service
        +create_booking(...)
        +cancel_booking(...)
    }

    class SearchController {
        -search_service
        +get_availability(...)
    }

    class TransactionController {
        -transaction_service
        +initiate_transaction(...)
        +handle_transaction_callback(...)
    }
    
    class DashboardController {
        -user_service
        +list_user_bookings(...)
    }

    %% Services
    class BookingService {
        +create_booking(...)
        +check_in(...)
        +check_out(...)
        +cancel_booking(...)
    }

    class InventoryService {
        +get_availability(...)
        +reduce_inventory(...)
    }

    class PricingService {
        +calculate_price(...)
    }

    class SearchService {
        +get_availability(...)
    }

    class TransactionService {
        +initiate_transaction(...)
        +handle_callback(...)
    }

    class UserService {
        +get_user_bookings(...)
    }

    %% Domains
    class Hotel {
        +id: String
        +name: String
        +address: String
        +rating: Float
        +is_active: Boolean
    }

    class RoomType {
        +id: String
        +hotel_id: String
        +name: String
        +capacity: int
        +base_price: Float
        +total_rooms: int
    }
    
    class Room {
        +id: String
        +hotel_id: String
        +room_type_id: String
        +room_number: String
        +is_active: Boolean
    }

    class Booking {
        +id: String
        +user_id: String
        +hotel_id: String
        +room_type_id: String
        +status: BookingStatus
        +total_price: Float
    }
    
    class User {
        +id: String
        +name: String
        +email: String
        +role: UserRole
    }
    
    class Transaction {
        +id: String
        +booking_id: String
        +amount: Float
        +status: TransactionStatus
    }

    %% Controllers depend on Services
    AdminController --> BookingService
    BookingController --> BookingService
    SearchController --> SearchService
    TransactionController --> TransactionService
    DashboardController --> UserService
    
    %% Services cross dependencies
    BookingService --> InventoryService
    BookingService --> PricingService
    BookingService --> TransactionService
    SearchService --> PricingService
    SearchService --> InventoryService
    TransactionService --> InventoryService
    
    %% Domain relationships
    Hotel "1" *-- "many" RoomType
    Hotel "1" *-- "many" Room
    RoomType "1" *-- "many" Room
    Booking "*" --> "1" RoomType : reserves
    Booking "*" --> "1" User : made by
    Transaction "*" --> "1" Booking : pays for
```

## Running the Simulation

A main executable simulation file `main.py` is provided to demonstrate the complete workflow. It initializes the mock database records, creates instances for dependency injection, and runs through several key scenarios:

1. Establishing a cancellation policy and a new Hotel.
2. Generating room types and registering users.
3. Defining dynamic pricing for specific rooms based on seasonal dates.
4. Simulating a room availability search by customer.
5. Creating bookings and handling payment transactions.
6. Simulating admin workflows like user check-in and check-out.
7. Generating the user's booking dashboard.

### Execution

Simply execute the main file:

```bash
python main.py
```
