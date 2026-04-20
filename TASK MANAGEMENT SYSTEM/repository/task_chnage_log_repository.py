


from typing import Dict, List

from domain.task_chnage_log import TaskChangeLog


class TaskChangeLogRepository:
    def __init__(self):
        self._logs: Dict[int, TaskChangeLog] = {}
        self._next_id = 1

    def save(self, log: TaskChangeLog) -> TaskChangeLog:
        if log.id == 0:
            new_log = TaskChangeLog(self._next_id, log.task_id, log.user_id, log.change_type, log.old_value, log.new_value)
            self._next_id += 1
            self._logs[new_log.id] = new_log
            return new_log
            
        self._logs[log.id] = log
        return log

    def find_by_task_id(self, task_id: int) -> List[TaskChangeLog]:
        return [log for log in self._logs.values() if log.task_id == task_id]
