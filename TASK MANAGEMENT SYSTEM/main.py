


from datetime import datetime, timedelta

from controller.task_assignment_controller import TaskAssignmentController
from controller.task_controller import TaskController
from controller.task_notification_controller import TaskNotificationController
from controller.task_state_controller import TaskStateController
from domain.comment import Comment
from domain.task_priority import Priority
from domain.task_search_criteria import TaskSearchCriteria
from domain.task_status import TaskStatus
from repository.comment_repository import CommentRepository
from repository.task_chnage_log_repository import TaskChangeLogRepository
from repository.task_repository_implementation import TaskRepositoryImpl
from repository.task_subscription_repository import TaskSubscriptionRepository
from repository.user_repository_implementation import UserRepositoryImpl
from service.task_assignment_service import TaskAssignmentService
from service.task_notification_service import TaskNotificationService
from service.task_service import TaskService
from service.task_state_service import TaskStateService


def simulate_user_dashboard(task_controller: TaskController, notification_controller: TaskNotificationController):
    print("User opens dashboard...")

    criteria = TaskSearchCriteria().assignee_id(1).status(TaskStatus.TODO)
    user_tasks = task_controller.search_tasks(criteria)
    print(f"📋 User has {len(user_tasks)} TODO tasks")

    if user_tasks:
        recent_changes = notification_controller.get_task_history(user_tasks[0].id)
        print(f"📢 Recent changes for first task: {len(recent_changes)} updates")

def simulate_task_creation(task_controller: TaskController, assignment_controller: TaskAssignmentController):
    print("User clicks 'Create New Task' button...")

    due_date = datetime.now() + timedelta(days=7)
    new_task = task_controller.create_task(
        "Implement User Authentication",
        "Create login, registration, and password reset functionality",
        due_date,
        "HIGH",
        1
    )
    print(f"✅ Task created: {new_task._title} (ID: {new_task._id})")

    print("User assigns task to team member...")
    assignment_controller.assign_task(new_task._id, 2)
    print("👤 Task assigned to user ID: 2")

    print("User adds subtask...")
    subtask = task_controller.add_subtask(
        new_task._id,
        "Design Database Schema",
        "Create user table and authentication tables",
        due_date - timedelta(days=2),
        "MEDIUM",
        1
    )
    print(f"📝 Subtask added: {subtask._title}")

def simulate_task_management(task_controller: TaskController, state_controller: TaskStateController, assignment_controller: TaskAssignmentController):
    print("User opens task management panel...")

    criteria = TaskSearchCriteria().status(TaskStatus.TODO)
    todo_tasks = task_controller.search_tasks(criteria)

    if todo_tasks:
        task_to_manage = todo_tasks[0]
        print(f"📋 Managing task: {task_to_manage._title}")

        print("User edits task details...")
        updated_task = task_controller.update_task(
            task_to_manage._id,
            f"{task_to_manage._title} (Updated)",
            f"{task_to_manage._description} - Additional requirements added",
            task_to_manage._due_date + timedelta(days=1),
            "HIGH"
        )
        print(f"✏️ Task updated: {updated_task._title}")

        print("User changes task status to In Progress...")
        state_controller.update_task_status(task_to_manage._id, TaskStatus.IN_PROGRESS)
        print("🔄 Task status changed to IN_PROGRESS")

        print("User reassigns task...")
        assignment_controller.assign_task(task_to_manage._id, 2)
        print("👤 Task reassigned to user ID: 2")

def simulate_task_collaboration(task_controller: TaskController, notification_controller: TaskNotificationController, comment_repository: CommentRepository):
    print("User opens task collaboration panel...")
    print("User subscribes to task notifications...")

    criteria = TaskSearchCriteria()
    available_tasks = task_controller.search_tasks(criteria)
    
    if available_tasks:
        task_id = available_tasks[0]._id
        notification_controller.subscribe_to_task(task_id, 2)
        print(f"🔔 User 2 subscribed to task {task_id}")

        task_history = notification_controller.get_task_history(task_id)
        print(f"📚 Task history retrieved: {len(task_history)} changes")
    else:
        print("⚠️ No tasks available for subscription")

    print("User adds comment to task...")
    comment = Comment(0, 1, 2, "Great progress! Let's review the implementation.")
    comment_repository.save(comment)
    print(f"💬 Comment added: {comment.content}")

def simulate_task_search(task_controller: TaskController):
    print("User searches for tasks...")

    high_priority_criteria = TaskSearchCriteria().priority(Priority.HIGH)
    high_priority_tasks = task_controller.search_tasks(high_priority_criteria)
    print(f"🔍 High priority tasks found: {len(high_priority_tasks)}")

    overdue_criteria = TaskSearchCriteria().status(TaskStatus.IN_PROGRESS)
    in_progress_tasks = task_controller.search_tasks(overdue_criteria)
    print(f"🔍 In-progress tasks found: {len(in_progress_tasks)}")

    complex_criteria = TaskSearchCriteria().assignee_id(1).status(TaskStatus.TODO).priority(Priority.MEDIUM)
    complex_search_results = task_controller.search_tasks(complex_criteria)
    print(f"🔍 Complex search results: {len(complex_search_results)} tasks")

    print("\n=== 🎯 STRATEGY PATTERN: Sorting Demonstrations ===")

    print("📊 Sorting by Priority (HIGH → MEDIUM → LOW):")
    priority_sort_criteria = TaskSearchCriteria().sort_by("priority").sort_order("desc")
    priority_sorted_tasks = task_controller.search_tasks(priority_sort_criteria)
    for task in priority_sorted_tasks:
        print(f"  - {task._title} (Priority: {task._priority.name})")

    print("\n📅 Sorting by Due Date (earliest first):")
    due_date_sort_criteria = TaskSearchCriteria().sort_by("due_date").sort_order("asc")
    due_date_sorted_tasks = task_controller.search_tasks(due_date_sort_criteria)
    for task in due_date_sorted_tasks:
        print(f"  - {task._title} (Due: {task._due_date})")

    print("\n🕒 Sorting by Created Date (newest first):")
    created_date_sort_criteria = TaskSearchCriteria().sort_by("created_date").sort_order("desc")
    created_date_sorted_tasks = task_controller.search_tasks(created_date_sort_criteria)
    for task in created_date_sorted_tasks:
        print(f"  - {task._title} (Created: {task._created_at})")

    print("\n✨ Strategy Pattern allows easy swapping of sorting algorithms at runtime!")

def simulate_notification_management(notification_controller: TaskNotificationController, task_controller: TaskController):
    print("User manages notification preferences...")
    print("User subscribes to multiple tasks...")

    for i in range(1, 3):
        notification_controller.subscribe_to_task(i, 1)
        print(f"🔔 Subscribed to task {i}")

    print("User unsubscribes from a task...")
    notification_controller.unsubscribe_from_task(2, 1)
    print("🔕 Unsubscribed from task 2")

    criteria = TaskSearchCriteria()
    available_tasks = task_controller.search_tasks(criteria)
    if available_tasks:
        task_id = available_tasks[0]._id
        notifications = notification_controller.get_task_history(task_id)
        print(f"📢 Notifications for task {task_id}: {len(notifications)} updates")
    else:
        print("⚠️ No tasks available for notification history")

    print("📱 Real-time notification received: Task status changed!")

if __name__ == "__main__":
    print("🚀 Starting Task Management System Simulation...\n")

    task_repository = TaskRepositoryImpl()
    user_repository = UserRepositoryImpl()
    change_log_repository = TaskChangeLogRepository()
    subscription_repository = TaskSubscriptionRepository()
    comment_repository = CommentRepository()

    task_service = TaskService(task_repository)
    assignment_service = TaskAssignmentService(task_repository, user_repository)
    state_service = TaskStateService(task_repository)
    notification_service = TaskNotificationService(subscription_repository, change_log_repository)

    task_controller = TaskController(task_service)
    assignment_controller = TaskAssignmentController(assignment_service)
    state_controller = TaskStateController(state_service)
    notification_controller = TaskNotificationController(notification_service)

    print("=== 📱 FRONTEND: User Dashboard ===")
    simulate_user_dashboard(task_controller, notification_controller)

    print("\n=== ✨ FRONTEND: Task Creation ===")
    simulate_task_creation(task_controller, assignment_controller)

    print("\n=== 🔄 FRONTEND: Task Management ===")
    simulate_task_management(task_controller, state_controller, assignment_controller)

    print("\n=== 👥 FRONTEND: Task Collaboration ===")
    simulate_task_collaboration(task_controller, notification_controller, comment_repository)

    print("\n=== 🔍 FRONTEND: Task Search ===")
    simulate_task_search(task_controller)

    print("\n=== 🔔 FRONTEND: Notifications ===")
    simulate_notification_management(notification_controller, task_controller)

    print("\n✅ Simulation completed successfully!")
