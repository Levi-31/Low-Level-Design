


from typing import Dict, Any

from service.rate_limiting_service import RateLimiterService

class RateLimiterController:
    def __init__(self, rate_limiter_service: RateLimiterService):
        # Entry Facade interface injection
        self._service = rate_limiter_service

    def handle_request(self, user_id: str) -> Dict[str, Any]:
        """
        Simulates an HTTP/API Gateway network controller interception interface.
        """
        is_allowed = self._service.check_rate_limit(user_id)
        if is_allowed:
            return {"status_code": 200, "body": "Request Authorized."}
        else:
            return {"status_code": 429, "body": "Too Many Requests. Limit Exceeded."}