from enum import IntEnum


class LogLevel(IntEnum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    FATAL = 5

    def __str__(self):
        return self.name
