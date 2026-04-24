


from dataclasses import dataclass, field
import time

from domain.audio_format import AudioFormat
from domain.audio_quality import AudioQuality

@dataclass
class Song:
    id: int
    song_id: str
    title: str
    artist_id: str
    album_id: str
    duration: int # in seconds
    audio_url: str
    thumbnail_url: str
    file_size: int
    quality: AudioQuality = AudioQuality.STANDARD
    format: AudioFormat = AudioFormat.MP3
    created_at: int = field(default_factory=lambda: int(time.time()))