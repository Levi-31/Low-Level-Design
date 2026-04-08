from abc import ABC, abstractmethod

from core.log_formatter import LogFormatter
from core.log_level import LogLevel
from core.log_message import LogMessage 


class LogAppender(ABC):
    @abstractmethod
    def append(self, log_message: LogMessage):
        pass

    @abstractmethod
    def set_level(self,log_message: LogLevel):
        pass

    @abstractmethod
    def get_level(self):
        pass

    @abstractmethod
    def is_enabled(self,level:LogLevel):
        pass

    @abstractmethod
    def set_formatter(self, formatter: LogFormatter):
        pass

    @abstractmethod
    def get_formatter(self) -> LogFormatter:
        pass



    