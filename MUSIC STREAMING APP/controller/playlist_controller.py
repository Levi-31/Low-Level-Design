


from typing import List

from domain.playlist import Playlist
from service.playlist_service import PlaylistService


class PlaylistController:
    def __init__(self, playlist_service: PlaylistService):
        self.playlist_service = playlist_service

    def create_playlist(self, user_id: int, name: str, song_ids: List[str]) -> Playlist:
        return self.playlist_service.create_playlist(user_id, name, song_ids)
    
    def update_playlist(self, playlist_id: str, user_id: int, name: str, song_ids: List[str]) -> Playlist:
        return self.playlist_service.update_playlist(playlist_id, user_id, name, song_ids)
    
    def delete_playlist(self, playlist_id: str, user_id: int) -> None:
        self.playlist_service.delete_playlist(playlist_id, user_id)

    def add_songs(self, playlist_id: str, user_id: int, song_ids: List[str]) -> Playlist:
        return self.playlist_service.add_songs(playlist_id, user_id, song_ids)

    def remove_songs(self, playlist_id: str, user_id: int, song_ids: List[str]) -> Playlist:
        return self.playlist_service.remove_songs(playlist_id, user_id, song_ids)