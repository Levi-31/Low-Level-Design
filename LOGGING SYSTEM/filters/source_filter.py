from core.log_filter import LogFilter
from core.log_level import LogLevel
from core.log_message import LogMessage

class SourceFilter(LogFilter):
    def __init__(self, source_pattern: str, include: bool):
        self.source_pattern = source_pattern
        self.include = include
        self.level = LogLevel.DEBUG

    def should_log(self, message: LogMessage) -> bool:
        if not message.source:
            return not self.include
        
        matches = self.source_pattern in message.source
        return matches if self.include else not matches

    def set_level(self, level: LogLevel): 
        self.level = level

    def get_level(self) -> LogLevel: 
        return self.level
