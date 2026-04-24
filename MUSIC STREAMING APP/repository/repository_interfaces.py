

from abc import ABC , abstractmethod
from typing import Optional, List

from domain.album import Album
from domain.artist import Artist
from domain.download import Download
from domain.listening_history import ListeningHistory
from domain.playback_session import PlaybackSession
from domain.playlist import Playlist
from domain.song import Song
from domain.user import User

class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User: pass
    
    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]: pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]: pass

class SongRepository(ABC):
    @abstractmethod
    def save(self, song: Song) -> Song: pass
    
    @abstractmethod
    def find_by_id(self, song_id: str) -> Optional[Song]: pass
    
    @abstractmethod
    def find_by_title(self, title: str) -> List[Song]: pass
    
    @abstractmethod
    def find_by_artist_id(self, artist_id: str) -> List[Song]: pass
    
    @abstractmethod
    def find_by_album_id(self, album_id: str) -> List[Song]: pass
    
    @abstractmethod
    def find_by_genre(self, genre: str) -> List[Song]: pass
    
    @abstractmethod
    def find_all_by_ids(self, song_ids: List[str]) -> List[Song]: pass

class AlbumRepository(ABC):
    @abstractmethod
    def save(self, album: Album) -> Album: pass
    
    @abstractmethod
    def find_by_id(self, album_id: str) -> Optional[Album]: pass
    
    @abstractmethod
    def find_by_artist_id(self, artist_id: str) -> List[Album]: pass
    
    @abstractmethod
    def find_by_title(self, title: str) -> List[Album]: pass

class ArtistRepository(ABC):
    @abstractmethod
    def save(self, artist: Artist) -> Artist: pass
    
    @abstractmethod
    def find_by_id(self, artist_id: str) -> Optional[Artist]: pass
    
    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Artist]: pass

class PlaylistRepository(ABC):
    @abstractmethod
    def save(self, playlist: Playlist) -> Playlist: pass
    
    @abstractmethod
    def find_by_id(self, playlist_id: str) -> Optional[Playlist]: pass
    
    @abstractmethod
    def find_by_user_id(self, user_id: int) -> List[Playlist]: pass
    
    @abstractmethod
    def remove(self, playlist_id: str) -> None: pass

class PlaybackSessionRepository(ABC):
    @abstractmethod
    def save(self, session: PlaybackSession) -> PlaybackSession: pass
    
    @abstractmethod
    def find_by_id(self, session_id: str) -> Optional[PlaybackSession]: pass
    
    @abstractmethod
    def find_by_user_id_and_device_id(self, user_id: int, device_id: str) -> Optional[PlaybackSession]: pass

class DownloadRepository(ABC):
    @abstractmethod
    def save(self, download: Download) -> Download: pass
    
    @abstractmethod
    def find_by_id(self, download_id: str) -> Optional[Download]: pass
    
    @abstractmethod
    def find_by_user_id(self, user_id: int) -> List[Download]: pass
    
    @abstractmethod
    def find_by_user_id_and_device_id(self, user_id: int, device_id: str) -> List[Download]: pass
    
    @abstractmethod
    def remove(self, download_id: str) -> None: pass

class ListeningHistoryRepository(ABC):
    @abstractmethod
    def save(self, history: ListeningHistory) -> ListeningHistory: pass
    
    @abstractmethod
    def find_by_user_id(self, user_id: int) -> List[ListeningHistory]: pass
    
    @abstractmethod
    def find_by_user_id_and_song_id(self, user_id: int, song_id: str) -> List[ListeningHistory]: pass
