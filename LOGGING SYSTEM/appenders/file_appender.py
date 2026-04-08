from core.log_appender import LogAppender
from core.log_level import LogLevel
from core.log_message import LogMessage
from formatters.simple_formatter import SimpleFormatter

class FileAppender(LogAppender):
    def __init__(self, file_path: str, level: LogLevel = LogLevel.DEBUG):
        self.file_path = file_path
        self.level = level
        self.formatter = SimpleFormatter()

    def append(self, message: LogMessage):
        if not self.is_enabled(message.level):
            return
        
        try:
            formatted = self.formatter.format(message)
            with open(self.file_path, "a") as f:
                f.write(formatted + "\n")
        except Exception as e:
            print(f"Failed to write to file {self.file_path}: {e}")

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
