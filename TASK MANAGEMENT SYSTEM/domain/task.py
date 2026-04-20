


from datetime import datetime
from typing import List

from domain.change_type import ChangeType
from domain.observer.task_subject import TaskSubject
from domain.observer.task_subscriber import TaskSubscriber
from domain.task_priority import Priority
from domain.task_status import TaskStatus


class Task(TaskSubject):
    def __init__(self, id: int, title: str, description: str, due_date: datetime, priority: Priority, creator_id: int, parent_task_id: int = 0):
        self._id = id
        self._title = title
        self._description = description
        self._due_date = due_date
        self._priority = priority
        self._status = TaskStatus.TODO
        self._assignee_id = 0
        self._creator_id = creator_id
        self._parent_task_id = parent_task_id
        self._tags: List[str] = []
        self._created_at = datetime.now()
        self._updated_at = datetime.now()
        
        self._subscribers: List[TaskSubscriber] = []
        self._subtasks: List['Task'] = []

    

    def attach(self, subscriber: TaskSubscriber):
        self._subscribers.append(subscriber)
    

    def detach(self, subscriber:TaskSubscriber):
        if subscriber in self._subscribers:
            self._subscribers.remove(subscriber)
    

    def notify_subscribers(self, change_type: ChangeType, old_value: str, new_value: str):
        for sub in self._subscribers:
            sub.update(self._id, change_type, old_value, new_value)
    

    # SUBTASK IMPLEMENTATION

    def add_subtask(self, task: 'Task'):
        self._subtasks.append(task)
        
    def get_subtasks(self) -> List['Task']:
        return self._subtasks

    def has_subtasks(self) -> bool:
        return len(self._subtasks) > 0

    def get_subtask_count(self) -> int:
        return len(self._subtasks)

    def get_all_subtasks(self) -> List['Task']:
        all_subtasks = []
        for st in self._subtasks:
            all_subtasks.append(st)
            all_subtasks.extend(st.get_all_subtasks())
        return all_subtasks

    def update_subtask_priorities(self):
        for subtask in self._subtasks:
            # Enums in Python priority.py: URGENT=4, HIGH=3, MEDIUM=2, LOW=1
            if subtask._priority.value > self._priority.value:
                self.priority = subtask._priority
            subtask.update_subtask_priorities()

