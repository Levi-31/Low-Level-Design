from typing import List
from domain.song import Song
from repository.repository_interfaces import ListeningHistoryRepository
from service.strategy.recommendation_strategy import RecommendationStrategy

class RecommendationService:
    def __init__(self, history_repo: ListeningHistoryRepository, strategy: RecommendationStrategy):
        self.history_repo = history_repo
        self.strategy = strategy

    def set_strategy(self, strategy: RecommendationStrategy) -> None:
        self.strategy = strategy

    def get_recommendations(self, user_id: int) -> List[Song]:
        history = self.history_repo.find_by_user_id(user_id)
        return self.strategy.generate(user_id, history)