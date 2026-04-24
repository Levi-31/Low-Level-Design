


import time 
from dataclasses import dataclass , field
from typing import List


@dataclass
class Playlist:
    id: int
    playlist_id: str
    name: str
    user_id: int
    is_public: bool = False
    song_ids: List[str] = field(default_factory=list)
    created_at: int = field(default_factory=lambda: int(time.time()))
    updated_at: int = field(default_factory=lambda: int(time.time()))