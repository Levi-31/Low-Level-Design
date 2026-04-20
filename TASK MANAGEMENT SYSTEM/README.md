# Task Management System (Low-Level Design)

A comprehensive Python-based Low-Level Design (LLD) implementation of a **Task Management System**. This project demonstrates clean architecture, solid design principles, and several Gang of Four (GoF) design patterns commonly expected in system design interviews.

## 🏗 Architecture Layers

The system follows a standard Layered Architecture:
1. **Controller Layer:** Entry points for user actions (e.g., `TaskController`, `TaskAssignmentController`).
2. **Service Layer:** Core business logic and use cases (e.g., `TaskService`, `TaskNotificationService`).
3. **Repository Layer:** Data access abstraction using Abstract Base Classes (e.g., `TaskRepository`, `UserRepository`) with in-memory implementations (`TaskRepositoryImpl`).
4. **Domain Layer:** Business models, entities, and enums (`Task`, `User`, `TaskStatus`, `Priority`).

## 🎨 Design Patterns Utilized

- **Observer Pattern:** Used to notify users when a task they are subscribed to is updated (e.g., status changes, re-assignments). Defined in `domain/observer`.
- **Strategy Pattern:** Used for dynamic and interchangeable sorting and searching algorithms within `TaskSearchCriteria`.
- **State Pattern:** Governs the lifecycle and valid status transitions of a `Task` (TODO → IN_PROGRESS → DONE).
- **Composite Pattern:** Enables hierarchical task structuring where a `Task` can contain multiple sub-Tasks (`_subtasks`).

## 📊 UML Class Diagram

```mermaid
classDiagram
    %% Core Entities
    class Task {
        -_id: int
        -_title: str
        -_description: str
        -_status: TaskStatus
        -_priority: Priority
        -_subtasks: List~Task~
        -_subscribers: List~TaskSubscriber~
        +add_subtask(task: Task)
        +attach(subscriber: TaskSubscriber)
        +detach(subscriber: TaskSubscriber)
        +notify_subscribers(change_type: ChangeType, old: str, new: str)
    }
    
    class User {
        -_id: int
        -_name: str
        -_email: str
        -_role: UserRole
    }
    
    class Comment {
        -_id: int
        -_task_id: int
        -_user_id: int
        -_content: str
    }

    %% Enums
    class TaskStatus {
        <<enumeration>>
        TODO
        IN_PROGRESS
        IN_REVIEW
        DONE
    }
    
    class Priority {
        <<enumeration>>
        LOW
        MEDIUM
        HIGH
        URGENT
    }

    %% Interfaces and Patterns
    class TaskSubject {
        <<interface>>
        +attach(subscriber: TaskSubscriber)
        +detach(subscriber: TaskSubscriber)
        +notify_subscribers(change_type: ChangeType, old: str, new: str)
    }
    
    class TaskSubscriber {
        <<interface>>
        +update(task_id: int, change_type: ChangeType, old: str, new: str)
    }

    %% Repositories
    class TaskRepository {
        <<interface>>
        +save(task: Task)
        +find_by_id(task_id: int)
        +search(criteria: TaskSearchCriteria)
    }
    
    class TaskRepositoryImpl {
        -tasks: dict
    }

    %% Services & Controllers
    class TaskService {
        -task_repository: TaskRepository
        +create_task(...)
        +search_tasks(criteria: TaskSearchCriteria)
    }
    
    class TaskController {
        -task_service: TaskService
        +create_task(...)
        +search_tasks(criteria: TaskSearchCriteria)
    }

    %% Relationships
    TaskSubject <|.. Task : implements
    Task *-- Task : contains subtasks (Composite)
    Task o-- TaskSubscriber : notifies (Observer)
    Task --> TaskStatus : status
    Task --> Priority : priority
    
    TaskRepository <|.. TaskRepositoryImpl : implements
    TaskService --> TaskRepository : uses
    TaskController --> TaskService : uses

    TaskSearchCriteria <.. TaskService : applies Strategy
```

## 🚀 How to Run

Navigate to the project directory and execute the simulation script:

```bash
cd "TASK MANAGEMENT SYSTEM"
python3 main.py
```

The output will simulate different scenarios including task creation, user assignments, dynamic sorting, and real-time collaboration updates.
