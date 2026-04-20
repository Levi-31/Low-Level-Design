


from typing import List
import uuid

from domain.topic import Topic
from repository.topic_repository import TopicRepository


class TopicService:
    def __init__(self, topic_repository: TopicRepository):
        self.topic_repository = topic_repository

    def create_topic(self, name: str) -> Topic:
        topic = Topic(str(uuid.uuid4()), name)
        return self.topic_repository.save(topic)

    def get_all_topics(self) -> List[Topic]:
        return self.topic_repository.find_all()

    def deactivate_topic(self, topic_id: str):
        topic = self.topic_repository.find_by_id(topic_id)
        if topic:
            topic.active = False