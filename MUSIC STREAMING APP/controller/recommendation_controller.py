


from typing import List

from domain.song import Song
from service.recommendation_servicce import RecommendationService


class RecommendationController:
    def __init__(self, recommendation_service: RecommendationService):
        self.recommendation_service = recommendation_service

    def get_recommendations(self, user_id: int) -> List[Song]:
        return self.recommendation_service.get_recommendations(user_id)