from dataclasses import dataclass, field
import time


@dataclass
class User:
    id: int
    username: str
    email: str
    name: str
    created_at: float = field(default_factory=time.time)