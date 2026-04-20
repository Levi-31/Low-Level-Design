




from typing import Dict, List, Optional

from domain.topic import Topic
from repository.topic_repository import TopicRepository


class TopicRepositoryImpl(TopicRepository):
    def __init__(self):
        self._topics: Dict[str, Topic] = {}

    def save(self, topic: Topic) -> Topic:
        self._topics[topic.id] = topic
        return topic

    def find_all(self) -> List[Topic]:
        return list(self._topics.values())

    def find_by_id(self, topic_id: str) -> Optional[Topic]:
        return self._topics.get(topic_id)

    def delete_by_id(self, topic_id: str):
        if topic_id in self._topics:
            del self._topics[topic_id]