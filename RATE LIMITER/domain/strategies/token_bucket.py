import time

from domain.tier_config import LimitConfig
from repository.rate_limiter_repository import RateLimiterRepository

class TokenBucketRateLimiter:
    def __init__(self):
        pass

    def _get_key(self, user_id: str, config: LimitConfig) -> str:
        return f"rate_limit:token_bucket:{user_id}:{config.window_seconds}"

    def is_allowed(self, user_id: str, config: LimitConfig, repository:RateLimiterRepository) -> bool:
        key = self._get_key(user_id, config)
        current_time = time.time()

        with repository.lock:
            state = repository.get_state(key)
            if state is None:
                # Fully pre-populated container initialization
                state = (float(config.max_requests), current_time)

            available_tokens, last_refill_time = state
            
            # Lazily calculate token replenishment based on elapsed time
            elapsed = current_time - last_refill_time
            refill_rate = config.max_requests / config.window_seconds
            
            # Replenish and cap at max capacity limit bounds
            available_tokens = min(float(config.max_requests), available_tokens + (elapsed * refill_rate))

            if available_tokens >= 1.0:
                repository.set_state(key, (available_tokens - 1.0, current_time))
                return True
            
            repository.set_state(key, (available_tokens, current_time))
            return False