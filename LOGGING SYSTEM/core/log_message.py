from dataclasses import dataclass, field
from datetime import datetime

from core.log_level import LogLevel

@dataclass(frozen=True)
class LogMessage:
    """
    Represents a single log entry.

    Using @dataclass:
    - Automatically generates __init__, __repr__, __eq__ methods
    - Reduces boilerplate code

    frozen=True:
    - Makes the instance immutable after creation
    - Prevents accidental modification of log data
    - Allows instances to be hashable (usable in sets/dicts)
    """

    # Log severity level (e.g., INFO, DEBUG, ERROR)
    # Expected to be an enum (LogLevel)
    level: LogLevel

    # Actual log message content
    message: str

    # Timestamp when the log is created
    # default_factory ensures datetime.now() is called at instance creation time
    # (NOT once at class definition time)
    timestamp: datetime = field(default_factory=datetime.now)

    # Source of the log (e.g., service name, module name)
    # Defaults to "UNKNOWN" if not provided
    source: str = "UNKNOWN"

    def __str__(self):
        return f"LogMessage{{level={self.level}, message='{self.message}', source='{self.source}'}}"
    

class LogMessageBuilder:
    def __init__(self):
        self._level = None
        self._message = None
        self._timestamp = datetime.now()
        self._source = "UNKNOWN"
    

    def level(self,level:LogLevel):
        self._level = level
        return self
    
    def message(self,message:str):
        self._message = message
        return self
    
    def source(self,source:str):
        self._source = source
        return self
    
    def timestamp(self,timestamp:datetime):
        self._timestamp = self.timestamp
        return self
    
    def build(self) -> LogMessage:
        if not self._level:
            raise ValueError("Log Level can't be  empty")
        
        if not self._message:
            raise ValueError("Log Message can't be empty")
        
        return LogMessage(
            level=self._level,
            message=self._message,
            timestamp=self._timestamp,
            source=self._source
        )
    



