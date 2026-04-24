


import time
from typing import List

from domain.playlist import Playlist
from repository.repository_interfaces import PlaylistRepository, SongRepository
from service.locking_service import LockingService


class PlaylistService:
    def __init__(self, playlist_repo: PlaylistRepository, song_repo: SongRepository, lock_service: LockingService):
        self.playlist_repo = playlist_repo
        self.song_repo = song_repo
        self.lock_service = lock_service


    def create_playlist(self, user_id: int, name: str, song_ids: List[str]) -> Playlist:
        if song_ids:
            songs = self.song_repo.find_all_by_ids(song_ids)
            if len(songs) != len(song_ids):
                raise ValueError("Some songs not found")

        now = int(time.time())
        playlist_id = f"PL_{now}"
        
        playlist = Playlist(
            id=0,
            playlist_id=playlist_id,
            name=name,
            user_id=user_id,
            is_public=False,
            song_ids=song_ids or [],
            created_at=now,
            updated_at=now
        )
        return self.playlist_repo.save(playlist)
    
    def update_playlist(self, playlist_id: str, user_id: int, name: str, song_ids: List[str]) -> Playlist:
        lock_key = f"playlist_lock_{playlist_id}"
        if not self.lock_service.acquire(lock_key, 500):
            raise RuntimeError("Playlist is being updated by another request")

        try:
            playlist = self.playlist_repo.find_by_id(playlist_id)
            if not playlist:
                raise ValueError(f"Playlist not found: {playlist_id}")
                
            if playlist.user_id != user_id:
                raise ValueError("User does not own this playlist")

            if song_ids:
                songs = self.song_repo.find_all_by_ids(song_ids)
                if len(songs) != len(song_ids):
                    raise ValueError("Some songs not found")

            if name:
                playlist.name = name
            if song_ids is not None:
                playlist.song_ids = song_ids
                
            playlist.updated_at = int(time.time())
            return self.playlist_repo.save(playlist)
        finally:
            self.lock_service.release(lock_key)

    def add_songs(self, playlist_id: str, user_id: int, song_ids: List[str]) -> Playlist:
        songs = self.song_repo.find_all_by_ids(song_ids)
        if len(songs) != len(song_ids):
            raise ValueError("Some songs not found")

        lock_key = f"playlist_lock_{playlist_id}"
        if not self.lock_service.acquire(lock_key, 500):
            raise RuntimeError("Playlist is being updated by another request")

        try:
            playlist = self.playlist_repo.find_by_id(playlist_id)
            if not playlist:
                raise ValueError(f"Playlist not found: {playlist_id}")
                
            if playlist.user_id != user_id:
                raise ValueError("User does not own this playlist")

            current_songs = list(playlist.song_ids)
            for song_id in song_ids:
                if song_id not in current_songs:
                    current_songs.append(song_id)
                    
            playlist.song_ids = current_songs
            playlist.updated_at = int(time.time())
            return self.playlist_repo.save(playlist)
        finally:
            self.lock_service.release(lock_key)


    def remove_songs(self, playlist_id: str, user_id: int, song_ids: List[str]) -> Playlist:
        lock_key = f"playlist_lock_{playlist_id}"
        if not self.lock_service.acquire(lock_key, 500):
            raise RuntimeError("Playlist is being updated by another request")

        try:
            playlist = self.playlist_repo.find_by_id(playlist_id)
            if not playlist:
                raise ValueError(f"Playlist not found: {playlist_id}")
                
            if playlist.user_id != user_id:
                raise ValueError("User does not own this playlist")

            current_songs = [s for s in playlist.song_ids if s not in song_ids]
            playlist.song_ids = current_songs
            playlist.updated_at = int(time.time())
            return self.playlist_repo.save(playlist)
        finally:
            self.lock_service.release(lock_key)


    def delete_playlist(self, playlist_id: str, user_id: int) -> None:
        playlist = self.playlist_repo.find_by_id(playlist_id)
        if not playlist:
            raise ValueError(f"Playlist not found: {playlist_id}")
            
        if playlist.user_id != user_id:
            raise ValueError("User does not own this playlist")
            
        self.playlist_repo.remove(playlist_id)