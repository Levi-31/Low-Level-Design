
from abc import ABC , abstractmethod
from typing import List

from domain.listening_history import ListeningHistory
from domain.song import Song

class RecommendationStrategy(ABC):
    @abstractmethod
    def generate(self, user_id: int, history: List[ListeningHistory]) -> List[Song]:
        pass

class GenreBasedStrategy(RecommendationStrategy):
    def generate(self, user_id: int, history: List[ListeningHistory]) -> List[Song]:
        # Mock implementation
        return []