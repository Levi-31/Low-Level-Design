





from typing import Dict, Optional

from domain.message import Message
from repository.message_repository import MessageRepository


class MessageRepositoryImpl(MessageRepository):
    def __init__(self):
        self._messages: Dict[str, Message] = {}

    def save(self, message: Message) -> Message:
        self._messages[message.id] = message
        return message

    def find_by_id(self, message_id: str) -> Optional[Message]:
        return self._messages.get(message_id)

    def delete_by_id(self, message_id: str):
        if message_id in self._messages:
            del self._messages[message_id]