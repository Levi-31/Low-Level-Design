

from typing import List, Optional

from domain.date_range import DateRange
from domain.task_priority import Priority
from domain.task_status import TaskStatus


class TaskSearchCriteria:
    def __init__(self):
        self._assignee_id: Optional[int] = None
        self._creator_id: Optional[int] = None
        self._priority: Optional[Priority] = None
        self._status: Optional[TaskStatus] = None
        self._due_date_range: Optional[DateRange] = None
        self._tags: List[str] = []
        self._has_subtasks: Optional[bool] = None
        
        self._sort_by: str = "priority"
        self._sort_order: str = "desc"

    def assignee_id(self, id: int) -> 'TaskSearchCriteria':
        self._assignee_id = id
        return self

    def creator_id(self, id: int) -> 'TaskSearchCriteria':
        self._creator_id = id
        return self

    def priority(self, priority: Priority) -> 'TaskSearchCriteria':
        self._priority = priority
        return self

    def status(self, status: TaskStatus) -> 'TaskSearchCriteria':
        self._status = status
        return self

    def due_date_range(self, range: DateRange) -> 'TaskSearchCriteria':
        self._due_date_range = range
        return self

    def tags(self, tags: List[str]) -> 'TaskSearchCriteria':
        self._tags = tags
        return self

    def has_subtasks(self, has: bool) -> 'TaskSearchCriteria':
        self._has_subtasks = has
        return self

    def sort_by(self, field: str) -> 'TaskSearchCriteria':
        self._sort_by = field
        return self

    def sort_order(self, order: str) -> 'TaskSearchCriteria':
        self._sort_order = order
        return self
    

    
    @property
    def get_assignee_id(self) -> Optional[int]: return self._assignee_id
    @property
    def get_creator_id(self) -> Optional[int]: return self._creator_id
    @property
    def get_priority(self) -> Optional[Priority]: return self._priority
    @property
    def get_status(self) -> Optional[TaskStatus]: return self._status
    @property
    def get_due_date_range(self) -> Optional[DateRange]: return self._due_date_range
    @property
    def get_tags(self) -> List[str]: return self._tags
    @property
    def get_has_subtasks(self) -> Optional[bool]: return self._has_subtasks
    @property
    def get_sort_by(self) -> str: return self._sort_by
    @property
    def get_sort_order(self) -> str: return self._sort_order
