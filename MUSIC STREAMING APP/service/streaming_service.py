


from domain.audio_quality import AudioQuality
from domain.subscription_tier import SubscriptionTier
from repository.repository_interfaces import SongRepository, UserRepository
from service.cache_service import CacheService


class StreamingService:
    def __init__(self, song_repo: SongRepository, user_repo: UserRepository, cache_service: CacheService):
        self.song_repo = song_repo
        self.user_repo = user_repo
        self.cache_service = cache_service

    def get_stream_url(self, song_id: str, user_id: int) -> str:
        song = self.song_repo.find_by_id(song_id)
        if not song:
            raise ValueError(f"Song not found: {song_id}")

        user = self.user_repo.find_by_id(user_id)
        quality = AudioQuality.STANDARD

        if user and user.subscription_tier == SubscriptionTier.PREMIUM:
            quality = AudioQuality.PREMIUM

        return f"{song.audio_url}?quality={quality.name}"

    def get_chunk(self, song_id: str, start: int, end: int) -> bytes:
        cached_chunk = self.cache_service.get_chunk(song_id, start, end)
        if cached_chunk:
            return cached_chunk

        chunk = bytes([0] * (end - start + 1)) # Mock fetch from CDN

        self.cache_service.put_chunk(song_id, start, end, chunk)

        return chunk

    def download_full_song(self, song_id: str, device_id: str) -> None:
        pass # Mock async download
