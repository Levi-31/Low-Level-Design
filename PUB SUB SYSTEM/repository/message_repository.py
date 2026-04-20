



from abc import ABC , abstractmethod
from typing import Optional

from domain.message import Message


class MessageRepository(ABC):
    @abstractmethod
    def save(self, message: Message) -> Message:
        pass

    @abstractmethod
    def find_by_id(self, message_id: str) -> Optional[Message]:
        pass

    @abstractmethod
    def delete_by_id(self, message_id: str):
        pass