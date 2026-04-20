


from abc import ABC , abstractmethod
from typing import List , Optional

from domain.topic import Topic


class TopicRepository(ABC):
    @abstractmethod
    def save(self, topic: Topic) -> Topic:
        pass

    @abstractmethod
    def find_all(self) -> List[Topic]:
        pass

    @abstractmethod
    def find_by_id(self, topic_id: str) -> Optional[Topic]:
        pass

    @abstractmethod
    def delete_by_id(self, topic_id: str):
        pass