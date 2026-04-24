

from dataclasses import dataclass, field
import time


@dataclass
class Artist:
    id: int
    artist_id: str
    name: str
    thumbnail_url: str
    created_at: int = field(default_factory=lambda: int(time.time()))