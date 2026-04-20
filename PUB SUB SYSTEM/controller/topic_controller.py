
from typing import List

from domain.topic import Topic
from service.topic_service import TopicService


class TopicController:
    def __init__(self, topic_service: TopicService):
        self.topic_service = topic_service

    def create_topic(self, name: str) -> Topic:
        return self.topic_service.create_topic(name)

    def get_all_topics(self) -> List[Topic]:
        return self.topic_service.get_all_topics()

    def deactivate_topic(self, topic_id: str):
        self.topic_service.deactivate_topic(topic_id)