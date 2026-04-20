



from abc import ABC, abstractmethod
from domain.message import Message


class SubscriberObserver(ABC):
    @abstractmethod
    def update(self, message: Message):
        pass