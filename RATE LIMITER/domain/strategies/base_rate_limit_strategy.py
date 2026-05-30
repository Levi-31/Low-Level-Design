
from abc import ABC ,abstractmethod

from domain.tier_config import LimitConfig
from repository.rate_limiter_repository import RateLimiterRepository

class RateLimitingStrategy(ABC):

    @abstractmethod
    def is_allowed(self,user_id:str, config: LimitConfig,repository:RateLimiterRepository) ->bool:
        """Evaluates bounds and mutates state inside the repository if valid."""
        pass
    

    # Completely optional to have this rollback method. 
    @abstractmethod
    def rollback(self, user_id: str, config: LimitConfig, repository:RateLimiterRepository) -> None:
        """Reverts the state inside the repository if a cascading rule constraint fails."""
        pass