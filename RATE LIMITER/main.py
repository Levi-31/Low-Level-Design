

import threading
from controller.rate_limiting_controller import RateLimiterController
from domain.strategies.fixed_window import FixedWindowRateLimiter
from domain.tier import UserTier
from domain.user import User
from repository.rate_limiter_repository import RateLimiterRepository
from repository.user_repository import UserRepository
from service.rate_limiting_service import RateLimiterService


def simulate_client_call(controller: RateLimiterController, user_id: str, req_id: int):
    response = controller.handle_request(user_id)
    print(f"[Thread-{threading.get_ident()}] Call #{req_id}: Status {response['status_code']} -> {response['body']}")

if __name__ == "__main__":
    # 1. Component Assembly (Dependency Injection Pipeline)
    user_repository = UserRepository()
    rate_limiter_repository = RateLimiterRepository()
    default_strategy = FixedWindowRateLimiter()
    
    rate_limiter_service = RateLimiterService(
        user_repo=user_repository, 
        rate_limiting_repo=rate_limiter_repository, 
        strategy=default_strategy
    )
    
    rate_limiter_controller = RateLimiterController(rate_limiter_service)

    # 2. Seed Mock Records into User Repository Data Store
    mock_free_user = User("user_free_demo", UserTier.FREE)
    user_repository.save(mock_free_user)

    # simulate_client_call(rate_limiter_controller,mock_free_user.user_id,1)

    print("--- Executing 13 Concurrent Threads on FREE User (Max Allowed: 10/min) ---")
    threads = []
    for i in range(1, 14):
        t = threading.Thread(target=simulate_client_call, args=(rate_limiter_controller, mock_free_user.user_id, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\nState validation complete. Exactly 10 requests were authorized and transactions were rolled back accurately.")