


import time
from typing import Tuple

from domain.strategies.base_rate_limit_strategy import RateLimitingStrategy
from domain.tier_config import LimitConfig
from repository.rate_limiter_repository import RateLimiterRepository


class FixedWindowRateLimiter(RateLimitingStrategy):
    def __init__(self):
        pass
    
    def _get_key(self, user_id: str, config: LimitConfig) -> str:
        current_time = time.time()
        window_bucket = int(current_time // config.window_seconds)
        
        return f"rate_limit:{user_id}:{config.window_seconds}:{window_bucket}"
    
    def is_allowed(self, user_id: str, config: LimitConfig, repository: RateLimiterRepository) -> bool:
        key = self._get_key(user_id, config)

        with repository.lock:
            current_count = repository.get_state(key, default=0)
            if current_count >= config.max_requests:
                return False
            
            repository.set_state(key, current_count + 1)
            return True
        

    def rollback(self,user_id:str,config: LimitConfig, repository) ->bool:
        pass