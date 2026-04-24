


from typing import List

from domain.album import Album
from domain.artist import Artist
from domain.song import Song
from repository.repository_interfaces import AlbumRepository, ArtistRepository, SongRepository


class SearchResponse:
    def __init__(self):
        self.songs: List[Song] = []
        self.artists: List[Artist] = []
        self.albums: List[Album] = []


class SearchService:
    def __init__(self, song_repo: SongRepository, artist_repo: ArtistRepository, album_repo: AlbumRepository):
        self.song_repo = song_repo
        self.artist_repo = artist_repo
        self.album_repo = album_repo


    def search(self, query: str, type: str) -> SearchResponse:
        response = SearchResponse()
        response.songs = self.song_repo.find_by_title(query)
        
        artist = self.artist_repo.find_by_name(query)
        if artist:
            response.artists.append(artist)
            
        response.albums = self.album_repo.find_by_title(query)
        return response