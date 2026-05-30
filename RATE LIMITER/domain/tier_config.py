



from typing import Dict, List

from domain.tier import UserTier


class LimitConfig:
    def __init__(self,max_requests:int, window_seconds:int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds


class TierLimits:
    
    TIER_LIMITS: Dict[UserTier, List[LimitConfig]] = {
        UserTier.FREE: [
            LimitConfig(max_requests=10, window_seconds=60),       # 10 req / minute
            LimitConfig(max_requests=100, window_seconds=86400)    # 100 req / day
        ],

        UserTier.PRO: [
            LimitConfig(max_requests=50, window_seconds=60),       # 50 req / minute
            LimitConfig(max_requests=500, window_seconds=86400)    # 500 req / day
        ],

        UserTier.MAX: [
            LimitConfig(max_requests=100, window_seconds=60),      # 100 req / minute
            LimitConfig(max_requests=1000, window_seconds=86400)   # 1000 req / day
        ]
    }

    @classmethod
    def get_limit_tier(self,user_tier:UserTier) -> List[LimitConfig]:

        return self.TIER_LIMITS.get(user_tier,[])
