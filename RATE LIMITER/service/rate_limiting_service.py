


import threading
from typing import Dict, List

from domain.strategies.base_rate_limit_strategy import RateLimitingStrategy
from domain.tier_config import LimitConfig, TierLimits
from repository.rate_limiter_repository import RateLimiterRepository
from repository.user_repository import UserRepository


class RateLimiterService:
    def __init__(self,user_repo: UserRepository,rate_limiting_repo : RateLimiterRepository, strategy: RateLimitingStrategy):
        self.user_repository = user_repo

        self.rate_limiting_repository = rate_limiting_repo

        self._rate_limiting_strategy = strategy

    
        self._master_lock = threading.Lock()
        self._user_locks: Dict[str, threading.Lock] = {}

    

    def _get_user_lock(self,user_id:str):

        with self._master_lock:
            if user_id not in self._user_locks:
                self._user_locks[user_id] = threading.Lock()
            
            return self._user_locks[user_id]
    

    def set_strategy(self,strategy: RateLimitingStrategy) -> None:
        self._rate_limiting_strategy = strategy
    

    def check_rate_limit(self,user_id:str):
        user = self.user_repository.find_by_id(user_id)
        if not user:
            return False 

        # 2. Resolve the limits matching this user's subscription tier
        limits = TierLimits.get_limit_tier(user.tier)

        with self._get_user_lock(user_id):
            for limit_config in limits:
                if not self._rate_limiting_strategy.is_allowed(user_id, limit_config, self.rate_limiting_repository):
                    return False 
            return True


