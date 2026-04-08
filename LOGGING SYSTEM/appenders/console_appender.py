

import sys

from core.log_appender import LogAppender
from core.log_level import LogLevel
from core.log_message import LogMessage
from formatters.simple_formatter import SimpleFormatter


class ConsoleAppender(LogAppender):
    def __init__(self, level: LogLevel = LogLevel.DEBUG):
        self.level = level
        self.formatter = SimpleFormatter()
        
    def append(self, message: LogMessage):
        if not self.is_enabled(message.level):
            return
        
        formatted = self.formatter.format(message)
        if message.level >= LogLevel.ERROR:
            print(formatted, file=sys.stderr)
        else:
            print(formatted)

            
    def set_level(self, level: LogLevel): 
        self.level = level

    def get_level(self) -> LogLevel: 
        return self.level
    
    def is_enabled(self, level: LogLevel) -> bool: 
        return level >= self.level
    
    def set_formatter(self, formatter): 
        self.formatter = formatter

    def get_formatter(self):  
        return self.formatter