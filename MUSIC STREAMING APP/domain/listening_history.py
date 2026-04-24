


from dataclasses import dataclass ,  field
import time 



@dataclass
class ListeningHistory:
    id: int
    user_id: int
    song_id: str
    play_duration: int
    completed: bool
    played_at: int = field(default_factory=lambda: int(time.time()))