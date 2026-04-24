





from dataclasses import dataclass , field
import time
from typing import List

from domain.playback_source import PlaybackSource
from domain.playback_status import PlaybackStatus
from domain.repeat_mode import RepeatMode


@dataclass
class PlaybackSession:
    id: int
    session_id: str
    user_id: int
    device_id: str
    current_song_id: str = ""
    current_position: int = 0
    source: PlaybackSource = PlaybackSource.SONG
    source_id: str = ""
    queue: List[str] = field(default_factory=list)
    shuffle_mode: bool = False
    repeat_mode: RepeatMode = RepeatMode.OFF
    status: PlaybackStatus = PlaybackStatus.STOPPED
    started_at: int = field(default_factory=lambda: int(time.time()))
    last_updated_at: int = field(default_factory=lambda: int(time.time()))