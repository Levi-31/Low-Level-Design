from abc import ABC, abstractmethod

from core.log_level import LogLevel
from core.log_message import LogMessage

class LogFilter(ABC):
    @abstractmethod
    def should_log(self, message: LogMessage) -> bool:
        pass

    @abstractmethod
    def set_level(self, level: LogLevel):
        pass

    @abstractmethod
    def get_level(self) -> LogLevel:
        pass
