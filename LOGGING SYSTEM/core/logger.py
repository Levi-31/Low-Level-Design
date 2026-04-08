from abc import ABC, abstractmethod
from typing import List

from core.log_appender import LogAppender
from core.log_filter import LogFilter
from core.log_level import LogLevel

class Logger(ABC):
    @abstractmethod
    def debug(self, message: str):
        pass

    @abstractmethod
    def info(self, message: str):
        pass

    @abstractmethod
    def warning(self, message: str):
        pass

    @abstractmethod
    def error(self, message: str):
        pass

    @abstractmethod
    def fatal(self, message: str):
        pass

    @abstractmethod
    def log(self, level: LogLevel, message: str):
        pass

    @abstractmethod
    def set_level(self, level: LogLevel):
        pass

    @abstractmethod
    def add_appender(self, appender: LogAppender):
        pass

    @abstractmethod
    def add_filter(self, log_filter: LogFilter):
        pass

    @abstractmethod
    def remove_filter(self, log_filter: LogFilter):
        pass

    @abstractmethod
    def get_appenders(self) -> List[LogAppender]:
        pass

    @abstractmethod
    def get_filters(self) -> List[LogFilter]:
        pass
