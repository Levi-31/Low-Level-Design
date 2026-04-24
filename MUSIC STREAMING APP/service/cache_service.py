
from typing import Dict, Optional
import time
import threading

class CacheEntry:
    def __init__(self, data: bytes):
        self.data = data
        self.last_accessed = time.time()

class CacheService:
    def __init__(self):
        self.cache: Dict[str, CacheEntry] = {}
        self.max_size = 1000
        self.lock = threading.Lock()

    def _build_key(self, song_id: str, start: int, end: int) -> str:
        return f"{song_id}_{start}_{end}"

    def _evict_lru(self) -> None:
        if not self.cache:
            return
        # Find least recently used
        lru_key = min(self.cache.items(), key=lambda x: x[1].last_accessed)[0]
        del self.cache[lru_key]

    def get_chunk(self, song_id: str, start: int, end: int) -> Optional[bytes]:
        with self.lock:
            key = self._build_key(song_id, start, end)
            entry = self.cache.get(key)
            if entry:
                entry.last_accessed = time.time()
                return entry.data
            return None

    def put_chunk(self, song_id: str, start: int, end: int, chunk: bytes) -> None:
        with self.lock:
            if len(self.cache) >= self.max_size:
                self._evict_lru()
            key = self._build_key(song_id, start, end)
            self.cache[key] = CacheEntry(chunk)

    def evict_chunk(self, song_id: str, start: int, end: int) -> None:
        with self.lock:
            key = self._build_key(song_id, start, end)
            self.cache.pop(key, None)

    def evict_song(self, song_id: str) -> None:
        with self.lock:
            prefix = f"{song_id}_"
            keys_to_remove = [k for k in self.cache.keys() if k.startswith(prefix)]
            for k in keys_to_remove:
                del self.cache[k]
