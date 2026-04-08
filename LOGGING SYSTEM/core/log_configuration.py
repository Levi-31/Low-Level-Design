

from core.log_level import LogLevel


class LogConfiguration:
    def __init__(self, root_level: LogLevel = LogLevel.INFO):
        self.root_level = root_level

    def get_root_level(self) -> LogLevel:
        return self.root_level

    def set_root_level(self, level: LogLevel):
        self.root_level = level

    def __str__(self):
        return f"LogConfiguration{{rootLevel={self.root_level}}}"
