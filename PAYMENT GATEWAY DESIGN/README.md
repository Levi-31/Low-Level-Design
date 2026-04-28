# Payment Gateway System - Low-Level Design (LLD)

A robust, highly modular Python-based Low-Level Design for a Payment Gateway System. The project simulates processing payments across multiple gateways (e.g., Razorpay, Paytm) and multiple payment methods (e.g., UPI, Credit Card, Net Banking) while handling concurrent requests gracefully.

---

## 🏗 System Architecture & Design Patterns

The architecture tightly follows **SOLID Principles** and uses a multi-layered design separating concerns between routing, business logic, integrations, and persistence.

### Layers
1. **Controller Layer (`payment_controller.py`)**: Acts as the entry point handling API/client requests and webhook callbacks.
2. **Service Layer (`payment_service.py`, `locking_service.py`)**: Houses the core business logic, controls transaction state, manages distributed locks to prevent race conditions, and coordinates with factories and strategies.
3. **Domain Layer (`domain/`)**: Contains pure dataclasses and Enums representing the business entities (`Transaction`, `PaymentRequest`, `PaymentResponse`, `User`, `TransactionStatus`).
4. **Repository Layer (`repository/`)**: In-memory storage components (`PaymentRepository`, `UserRepository`) mimicking a database to store and retrieve states.

### Design Patterns Utilized
- **Strategy Pattern (`PaymentStrategy`)**: Allows the system to dynamically execute different payment logic (UPI, NetBanking, Credit Card) without polluting the main service logic with `if/else` checks.
- **Factory Pattern (`PaymentFactory`)**: Encapsulates the instantiation logic for creating `PaymentGateway` and `PaymentStrategy` instances based on user requests.
- **Template Method / Interface (`PaymentGateway`)**: Defines a standardized contract (`create_order`, `authorize`, `capture`) that any external provider (Razorpay, Paytm) must adhere to, making the system extensible.

---

## 🔄 Execution Flow Diagram

The sequence diagram below visualizes the flow of a standard payment request, from the moment a client initiates it to the moment a response is returned.

```mermaid
sequenceDiagram
    participant Client
    participant Controller as PaymentController
    participant Service as PaymentService
    participant Lock as LockService
    participant Factory as PaymentFactory
    participant Strategy as PaymentStrategy (e.g. UPI)
    participant Repo as PaymentRepository

    Client->>Controller: process_payment(PaymentRequest)
    Controller->>Service: process_payment(PaymentRequest)
    
    Service->>Repo: find_by_id(user_id) (Validate User)
    Service->>Lock: acquire("req:uuid") (Thread Safety)
    
    Service->>Factory: get_payment_strategy(gateway, method)
    Factory-->>Service: PaymentStrategy & Gateway instance
    
    Service->>Repo: save(Transaction STATUS: INITIATED)
    
    Service->>Strategy: process_payment(PaymentRequest, Transaction)
    Strategy-->>Service: PaymentResponse (STATUS: PENDING)
    
    Service->>Repo: save(Transaction updated with gateway_id)
    Service->>Lock: release("req:uuid")
    
    Service-->>Controller: PaymentResponse
    Controller-->>Client: PaymentResponse
```

---

## 📊 UML Class Diagram

```mermaid
classDiagram
    class PaymentController {
        +PaymentService payment_service
        +process_payment(payment_request: PaymentRequest) PaymentResponse
        +handle_payment_callback(provider_ref: str, status: TransactionStatus) void
    }

    class PaymentService {
        +PaymentRepository payment_repository
        +UserRepository user_repository
        +LockService locking_service
        +get_payment_strategy(payment_request: PaymentRequest) PaymentStrategy
        +process_payment(payment_request: PaymentRequest) PaymentResponse
        +handle_call_back(gateway_transaction_id: str, status: TransactionStatus) void
    }

    class PaymentFactory {
        +get_gateway(name: Enum) PaymentGateway$
        +get_payment_strategy(payment_method: Enum, gateway: PaymentGateway) PaymentStrategy$
    }

    class PaymentGateway {
        <<interface>>
        +create_order(payment)
        +authorize(payment)
        +capture(payment)
        +verify_webhook(payload, signature) bool
        +supports(method: PaymentMethod) bool
    }

    class RazorpayGateway {
        +PaymentGateWays name
    }

    class PaytmGateway {
        +PaymentGateWays name
    }

    class PaymentStrategy {
        <<interface>>
        +PaymentGateway gateway
        +process_payment(payment_request: PaymentRequest, transaction: Transaction) PaymentResponse
    }

    class UPIPayment {
        +process_payment(...) PaymentResponse
    }

    class NetBankingPayment {
        +process_payment(...) PaymentResponse
    }

    class CreditCardPayment {
        +process_payment(...) PaymentResponse
    }

    class PaymentRepository {
        -Dict _transactions_by_id
        -Dict _transaction_id_by_provider_ref
        +save(transaction: Transaction) Transaction
        +find_by_id(transaction_id: str) Transaction
        +find_by_gateway_transaction_id(id: str) Transaction
    }

    class UserRepository {
        -Dict _users_by_id
        +save(user: User) User
        +find_by_id(user_id: int) User
    }

    class LockService {
        -Dict _lock_map
        -Lock _map_lock
        +acquire(key: str, timeout_ms: int) bool
        +release(key: str) void
    }

    class Transaction {
        +str id
        +str payment_id
        +PaymentGateWays gateway
        +PaymentMethod payment_method
        +TransactionStatus status
        +int user_id
        +str request_id
        +str gateway_transaction_id
        +update_status(new_status: TransactionStatus)
    }

    class PaymentRequest {
        +str sender
        +str receiver
        +float amount
        +str currency
        +PaymentGateWays gateway
        +PaymentMethod payment_method
        +int user_id
        +str request_id
    }

    class PaymentResponse {
        +str payment_id
        +str status
        +float amount
        +str currency
        +str gateway
        +str payment_method
        +str message
        +str transaction_id
    }

    %% Relationships
    PaymentController --> PaymentService
    PaymentService --> PaymentFactory
    PaymentService --> PaymentRepository
    PaymentService --> UserRepository
    PaymentService --> LockService
    PaymentService --> PaymentStrategy
    
    PaymentFactory ..> PaymentGateway : creates
    PaymentFactory ..> PaymentStrategy : creates
    
    PaymentStrategy --> PaymentGateway
    PaymentGateway <|-- RazorpayGateway
    PaymentGateway <|-- PaytmGateway
    
    PaymentStrategy <|-- UPIPayment
    PaymentStrategy <|-- NetBankingPayment
    PaymentStrategy <|-- CreditCardPayment
    
    PaymentRepository --> Transaction
    UserRepository --> User
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+

### Execution
Run the system using the provided entry point:

```bash
python3 main.py
```

### Example Output
When executing `main.py`, you will see a complete lifecycle simulation including User creation, Payment Initialization, and an incoming Webhook simulating success:

```
=== Initializing Payment Gateway System ===

--- Creating User ---
User created: John Doe (ID: 1)

--- Creating Payment Request (Request ID: 1234-abcd-5678-efgh) ---

--- Processing Payment ---
[UPI] Initiating payment for user 1
[UPI] Creating collect request
[UPI] Sending request to PSP
[UPI] Waiting for user approval (callback expected)
Payment Response:
  Payment ID: pay_1234-abcd-5678-efgh
  Status: PENDING
  Transaction ID: txn_1234-abcd-5678-efgh
  Message: UPI collect request sent

--- Simulating Webhook Callback from Payment Gateway ---
Received webhook for Gateway Transaction ID: upi_txn_9876-zyxw-4321-vuts
Transaction Status after callback: SUCCESS
```
