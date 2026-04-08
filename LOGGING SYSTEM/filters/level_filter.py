from core.log_filter import LogFilter
from core.log_level import LogLevel
from core.log_message import LogMessage

class LevelFilter(LogFilter):
    def __init__(self, level: LogLevel = LogLevel.DEBUG):
        self.level = level

    def should_log(self, message: LogMessage) -> bool:
        return message.level >= self.level

    def set_level(self, level: LogLevel): 
        self.level = level

    def get_level(self) -> LogLevel: 
        return self.level
