# Notification System - System Architecture & Design

This document provides a comprehensive overview of the Notification System, covering its layered architecture, entities, and the core design patterns used to ensure modularity, scalability, and adherence to the Open/Closed Principle.

## 1. Architectural Flow (Block Diagram)

The following block diagram represents the execution flow from the moment a notification is triggered by the client until it is dispatched to the users via their preferred channels.

```mermaid
graph TD
    Client[Client / Application Entry Point] -->|1. Triggers| Ctrl(NotificationController)
    Ctrl -->|2. send_notification| Svc(NotificationService)
    
    subgraph Service Layer
        Svc -->|3a. Wraps content| Dec[Decorator Pattern <br/> SimpleNotification <br/>↓<br/> TimeStampDecorator <br/>↓<br/> SignatureDecorator]
        Dec -->|3b. Generates| Msg(NotificationMessage)
    end
    
    Svc -->|4. save| Repo[(NotificationRepository)]
    
    Svc -->|5. notify| Obs(NotificationObservable)
    
    subgraph Observer Layer
        Obs -->|6a. update| Log(Logger Observer)
        Obs -->|6b. update| Eng(NotificationEngine Observer)
    end
    
    subgraph Strategy Layer
        Eng -->|7. Resolves Channels| StratMap{Strategy Map <br/> via NotificationStrategy}
        StratMap -->|EMAIL| EStrat[EmailStrategy]
        StratMap -->|SMS| SStrat[SMSStrategy]
        StratMap -->|PUSH| PStrat[PushStrategy]
    end
```

### Flow Explanation:
1. **Triggering**: The client (or `main.py`) calls the `NotificationController` to send a notification to a list of users.
2. **Processing**: The controller delegates the task to the `NotificationService`.
3. **Decorating**: The service takes the raw text and dynamically adds features (Timestamp and Signature) using the **Decorator Pattern**. It then packages this content and the target users into a `NotificationMessage` domain entity.
4. **Persistence**: The service saves the generated message to the database via the `NotificationRepository`.
5. **Notification**: The service triggers the `NotificationObservable` (Publisher).
6. **Observation**: The `NotificationObservable` notifies all registered subscribers (**Observer Pattern**). In this system, the `Logger` records the event, and the `NotificationEngine` handles the delivery.
7. **Delivery**: The `NotificationEngine` looks at each user's preferred channels and utilizes the **Strategy Pattern** to select the correct delivery mechanism (Email, SMS, or Push) dynamically.

---

## 2. UML Class Diagram

This class diagram visualizes the object-oriented structure of the project, including relationships (Inheritance, Composition, and Aggregation) and the interfaces for the design patterns used.

```mermaid
classDiagram
    %% Domain Entities
    class Subscriber {
        +user_id: str
        +channels: List[NotificationChannel]
    }
    
    class NotificationChannel {
        <<enumeration>>
        EMAIL
        SMS
        PUSH
    }

    %% Decorator Pattern Hierarchy
    class BaseNotification {
        <<abstract>>
        +get_content() str*
    }

    class SimpleNotification {
        +text: str
        +get_content() str
    }

    class NotificationDecorator {
        +notification: BaseNotification
        +get_content() str
    }

    class TimeStampDecorator {
        +get_content() str
    }

    class SignatureDecorator {
        +get_content() str
    }

    class NotificationMessage {
        +content: BaseNotification
        +users: List[Subscriber]
        +get_message() str
    }

    %% Repository Layer
    class NotificationRepository {
        +storage: List[NotificationMessage]
        +save(notification: NotificationMessage)
        +get_all() List[NotificationMessage]
    }

    %% Service Layer
    class NotificationService {
        +repo: NotificationRepository
        +observable: NotificationObservable
        +process_notification(text: str, users: List[Subscriber])
    }

    %% Controller Layer
    class NotificationController {
        +service: NotificationService
        +send_notification(text: str, users: List[Subscriber])
    }

    %% Observer Pattern Hierarchy
    class NotificationObservable {
        +observers: List[NotificationObserver]
        +add(observer: NotificationObserver)
        +notify(notification: NotificationMessage)
    }

    class NotificationObserver {
        <<abstract>>
        +update(notification: NotificationMessage)*
    }

    class Logger {
        +update(notification: NotificationMessage)
    }

    class NotificationEngine {
        +strategy_map: Dict[NotificationChannel, NotificationStrategy]
        +update(notification: NotificationMessage)
    }

    %% Strategy Pattern Hierarchy
    class NotificationStrategy {
        <<abstract>>
        +channel() NotificationChannel*
        +send(user: Subscriber, content: str)*
    }

    class EmailStrategy {
        +channel() NotificationChannel
        +send(user: Subscriber, content: str)
    }

    class SMSStrategy {
        +channel() NotificationChannel
        +send(user: Subscriber, content: str)
    }

    class PushStrategy {
        +channel() NotificationChannel
        +send(user: Subscriber, content: str)
    }

    %% Structural Relationships
    Subscriber --> NotificationChannel
    NotificationMessage --> BaseNotification
    NotificationMessage o-- Subscriber : has
    
    %% Decorator Relationships
    BaseNotification <|-- SimpleNotification : implements
    BaseNotification <|-- NotificationDecorator : implements
    NotificationDecorator o-- BaseNotification : wraps
    NotificationDecorator <|-- TimeStampDecorator : extends
    NotificationDecorator <|-- SignatureDecorator : extends
    
    %% Architectural Injection
    NotificationService --> NotificationRepository : uses
    NotificationService --> NotificationObservable : uses
    NotificationController --> NotificationService : uses
    
    %% Observer Relationships
    NotificationObservable o-- NotificationObserver : contains
    NotificationObserver <|-- Logger : implements
    NotificationObserver <|-- NotificationEngine : implements
    
    %% Strategy Relationships
    NotificationEngine o-- NotificationStrategy : aggregates
    NotificationEngine --> NotificationChannel : depends on
    NotificationStrategy <|-- EmailStrategy : implements
    NotificationStrategy <|-- SMSStrategy : implements
    NotificationStrategy <|-- PushStrategy : implements
```

## 3. Key Design Patterns Utilized

1. **Strategy Pattern**
   - **Where:** `service/strategy/`
   - **Why:** Allows adding new notification channels without altering existing delivery logic. The `NotificationEngine` dynamically resolves the correct strategy using the Enum as a key.
2. **Observer Pattern**
   - **Where:** `service/observer/`
   - **Why:** Separates the core notification persistence/generation from downstream effects. Adding a new behavior (like a metric tracker or an external webhook) simply requires creating a new `NotificationObserver` and adding it to the `NotificationObservable`.
3. **Decorator Pattern**
   - **Where:** `service/decorator/`
   - **Why:** Prevents "class explosion" when adding features to a message (e.g., trying to maintain `TimeStampSignatureNotification`, `TimeStampNotification`, etc.). It allows combining message augmentations recursively at runtime.
