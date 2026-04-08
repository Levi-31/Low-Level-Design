


import inspect
import threading
from typing import List

from appenders.console_appender import ConsoleAppender
from core.log_appender import LogAppender
from core.log_configuration import LogConfiguration
from core.log_filter import LogFilter
from core.log_level import LogLevel
from core.log_message import LogMessageBuilder
from core.logger import Logger


class LoggerImplementation(Logger):
    def __init__(self, name:str = "DefaultLogger", add_default_appender:bool = True, config:LogConfiguration=None):
        self.name = name
        self.level = LogLevel.INFO if config is None else config.get_root_level()
        self.appenders: List[LogAppender] = []
        self.filters: List[LogFilter] = []
        self._lock = threading.Lock()

        if add_default_appender:
            self.add_appender(ConsoleAppender())

    def debug(self, message: str): 
        self.log(LogLevel.DEBUG, message)

    def info(self, message: str): 
        self.log(LogLevel.INFO, message)

    def warning(self, message: str): 
        self.log(LogLevel.WARNING, message)

    def error(self, message: str): 
        self.log(LogLevel.ERROR, message)

    def fatal(self, message: str): 
        self.log(LogLevel.FATAL, message)
    

    def log(self, log_level:LogLevel, message:str):
        with self._lock:
            if log_level < self.level: #low priority log has came
                return 
            
            log_message = LogMessageBuilder().level(log_level).message(message).source(self._get_calling_class()).build()

            for filter in self.filters:
                if not filter.should_log():
                    return
            
            for appender in self.appenders:
                if appender.is_enabled(log_level):
                    appender.append(log_message)


    def set_level(self, level: LogLevel):
        with self._lock:
            self.level = level

    def add_appender(self, appender: LogAppender):
        with self._lock:
            self.appenders.append(appender)

    def add_filter(self, log_filter: LogFilter):
        with self._lock:
            self.filters.append(log_filter)

    def remove_filter(self, log_filter: LogFilter):
        with self._lock:
            if log_filter in self.filters:
                self.filters.remove(log_filter)

    def get_appenders(self) -> List[LogAppender]:
        with self._lock:
            return list(self.appenders)

    def get_filters(self) -> List[LogFilter]:
        with self._lock:
            return list(self.filters)
        
    def _get_calling_class(self) -> str:
        try:
            stack = inspect.stack()
            # stack[0] is this method, stack[1] is log(), stack[2] is info/error etc, stack[3] is caller
            if len(stack) > 3:
                frame = stack[3]
                module = inspect.getmodule(frame[0])
                module_name = module.__name__ if module else "Unknown"
                return f"{module_name}.{frame.function}"
        except Exception:
            pass
        return "Unknown"