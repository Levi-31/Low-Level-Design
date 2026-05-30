


import time
from typing import List

from domain.strategies.base_rate_limit_strategy import RateLimitingStrategy
from domain.tier_config import LimitConfig
from repository.rate_limiter_repository import RateLimiterRepository


class SlidingWindowLogRateLimiter(RateLimitingStrategy):
    def __init__(self):
        pass

    def _get_key(self, user_id: str, config: LimitConfig) -> str:
        # The key simply isolates the user and the specific time window duration.
        return f"rate_limit:sliding:{user_id}:{config.window_seconds}"

    def is_allowed(self, user_id:str, config:LimitConfig, repository:RateLimiterRepository):
        key = self._get_key(user_id,config)

        current_time = time.time()

        # Calculate the threshold boundary (e.g., 60 seconds ago from right now)
        sliding_window_start = current_time - config.window_seconds

        with repository.lock:
            timestamp_log: List[float] = repository.get_state(key, default=[])

            # 2. Evict phase: Filter out and remove any timestamps older than our rolling window start
            # This naturally slides the window forward in real-time

            active_timestamps = [t for t in timestamp_log if t >= sliding_window_start]

            # 3. Admission Control: Check if the remaining active requests hit the ceiling limit
            if len(active_timestamps) >= config.max_requests:
                # Even if blocked, update repository to keep memory clean of expired timestamps
                repository.set_state(key, active_timestamps)
                return False
            
            # 4. Commit Phase: Append the current request's timestamp to the active log
            active_timestamps.append(current_time)
            repository.set_state(key, active_timestamps)
            return True
        
    def rollback(self,user_id:str,config: LimitConfig, repository:RateLimiterRepository) ->bool:
        pass

