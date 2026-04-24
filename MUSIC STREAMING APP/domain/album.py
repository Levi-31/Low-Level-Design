

from dataclasses import dataclass, field
import time


@dataclass
class Album:
    id: int
    album_id: str
    title: str
    artist_id: str
    thumbnail_url: str
    created_at: int = field(default_factory=lambda: int(time.time()))
