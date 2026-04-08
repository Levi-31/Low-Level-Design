

from core.log_formatter import LogFormatter
from core.log_message import LogMessage


class DetailedFormatter(LogFormatter):
    def __init__(self, pattern: str = "[%LEVEL] %TIMESTAMP [%SOURCE] - %MESSAGE"):
        self.pattern = pattern
        self.date_format = "%Y-%m-%d %H:%M:%S"

    def format(self, message: LogMessage) -> str:
        if not self.pattern:
            source = message.source if message.source else "Unknown"
            return f"[{message.level}] {message.timestamp} [{source}] - {message.message}"
        
        formatted = self.pattern
        formatted = formatted.replace("%LEVEL", str(message.level))
        formatted = formatted.replace("%TIMESTAMP", message.timestamp.strftime(self.date_format))
        formatted = formatted.replace("%MESSAGE", message.message)
        formatted = formatted.replace("%SOURCE", message.source if message.source else "Unknown")
        return formatted

    def set_pattern(self, pattern: str): 
        self.pattern = pattern

    def get_pattern(self) -> str: 
        return self.pattern
    
    def set_date_format(self, date_format: str): 
        self.date_format = date_format
