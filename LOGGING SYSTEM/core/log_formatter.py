from abc import ABC, abstractmethod


class LogFormatter(ABC):
    
    @abstractmethod
    def format(self, message: LogMessage) -> str:
        pass

    @abstractmethod
    def set_pattern(self, pattern: str):
        pass

    @abstractmethod
    def get_pattern(self) -> str:
        pass

    @abstractmethod
    def set_date_format(self, date_format: str):
        pass
    