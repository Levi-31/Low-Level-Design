




import threading
from typing import List, Optional

from domain.album import Album
from domain.artist import Artist
from domain.download import Download
from domain.listening_history import ListeningHistory
from domain.playback_session import PlaybackSession
from domain.playlist import Playlist
from domain.song import Song
from domain.user import User
from repository.repository_interfaces import AlbumRepository, ArtistRepository, DownloadRepository, ListeningHistoryRepository, PlaybackSessionRepository, PlaylistRepository, SongRepository, UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = {}
        self.email_to_id = {}
        self.lock = threading.Lock()

    def save(self, user: User) -> User:
        with self.lock:
            if not user.id:
                user.id = len(self.users) + 1
            self.users[user.id] = user
            self.email_to_id[user.email] = user.id
            return user

    def find_by_id(self, user_id: int) -> Optional[User]:
        with self.lock:
            return self.users.get(user_id)

    def find_by_email(self, email: str) -> Optional[User]:
        with self.lock:
            user_id = self.email_to_id.get(email)
            return self.users.get(user_id) if user_id else None

class InMemorySongRepository(SongRepository):
    def __init__(self):
        self.songs = {}
        self.lock = threading.Lock()

    def save(self, song: Song) -> Song:
        with self.lock:
            self.songs[song.song_id] = song
            return song

    def find_by_id(self, song_id: str) -> Optional[Song]:
        with self.lock:
            return self.songs.get(song_id)

    def find_by_title(self, title: str) -> List[Song]:
        with self.lock:
            return [s for s in self.songs.values() if title.lower() in s.title.lower()]

    def find_by_artist_id(self, artist_id: str) -> List[Song]:
        with self.lock:
            return [s for s in self.songs.values() if s.artist_id == artist_id]

    def find_by_album_id(self, album_id: str) -> List[Song]:
        with self.lock:
            return [s for s in self.songs.values() if s.album_id == album_id]

    def find_by_genre(self, genre: str) -> List[Song]:
        with self.lock:
            return list(self.songs.values()) # Simplified for LLD

    def find_all_by_ids(self, song_ids: List[str]) -> List[Song]:
        with self.lock:
            return [self.songs[sid] for sid in song_ids if sid in self.songs]

class InMemoryAlbumRepository(AlbumRepository):
    def __init__(self):
        self.albums = {}
        self.lock = threading.Lock()

    def save(self, album: Album) -> Album:
        with self.lock:
            self.albums[album.album_id] = album
            return album

    def find_by_id(self, album_id: str) -> Optional[Album]:
        with self.lock:
            return self.albums.get(album_id)

    def find_by_artist_id(self, artist_id: str) -> List[Album]:
        with self.lock:
            return [a for a in self.albums.values() if a.artist_id == artist_id]

    def find_by_title(self, title: str) -> List[Album]:
        with self.lock:
            return [a for a in self.albums.values() if title.lower() in a.title.lower()]

class InMemoryArtistRepository(ArtistRepository):
    def __init__(self):
        self.artists = {}
        self.lock = threading.Lock()

    def save(self, artist: Artist) -> Artist:
        with self.lock:
            self.artists[artist.artist_id] = artist
            return artist

    def find_by_id(self, artist_id: str) -> Optional[Artist]:
        with self.lock:
            return self.artists.get(artist_id)

    def find_by_name(self, name: str) -> Optional[Artist]:
        with self.lock:
            for artist in self.artists.values():
                if artist.name.lower() == name.lower():
                    return artist
            return None

class InMemoryPlaylistRepository(PlaylistRepository):
    def __init__(self):
        self.playlists = {}
        self.lock = threading.Lock()

    def save(self, playlist: Playlist) -> Playlist:
        with self.lock:
            self.playlists[playlist.playlist_id] = playlist
            return playlist

    def find_by_id(self, playlist_id: str) -> Optional[Playlist]:
        with self.lock:
            return self.playlists.get(playlist_id)

    def find_by_user_id(self, user_id: int) -> List[Playlist]:
        with self.lock:
            return [p for p in self.playlists.values() if p.user_id == user_id]

    def remove(self, playlist_id: str) -> None:
        with self.lock:
            if playlist_id in self.playlists:
                del self.playlists[playlist_id]

class InMemoryPlaybackSessionRepository(PlaybackSessionRepository):
    def __init__(self):
        self.sessions = {}
        self.lock = threading.Lock()

    def save(self, session: PlaybackSession) -> PlaybackSession:
        with self.lock:
            self.sessions[session.session_id] = session
            return session

    def find_by_id(self, session_id: str) -> Optional[PlaybackSession]:
        with self.lock:
            return self.sessions.get(session_id)

    def find_by_user_id_and_device_id(self, user_id: int, device_id: str) -> Optional[PlaybackSession]:
        with self.lock:
            for s in self.sessions.values():
                if s.user_id == user_id and s.device_id == device_id:
                    return s
            return None

class InMemoryDownloadRepository(DownloadRepository):
    def __init__(self):
        self.downloads = {}
        self.lock = threading.Lock()

    def save(self, download: Download) -> Download:
        with self.lock:
            self.downloads[download.download_id] = download
            return download

    def find_by_id(self, download_id: str) -> Optional[Download]:
        with self.lock:
            return self.downloads.get(download_id)

    def find_by_user_id(self, user_id: int) -> List[Download]:
        with self.lock:
            return [d for d in self.downloads.values() if d.user_id == user_id]

    def find_by_user_id_and_device_id(self, user_id: int, device_id: str) -> List[Download]:
        with self.lock:
            return [d for d in self.downloads.values() if d.user_id == user_id and d.device_id == device_id]

    def remove(self, download_id: str) -> None:
        with self.lock:
            if download_id in self.downloads:
                del self.downloads[download_id]

class InMemoryListeningHistoryRepository(ListeningHistoryRepository):
    def __init__(self):
        self.histories = []
        self.lock = threading.Lock()

    def save(self, history: ListeningHistory) -> ListeningHistory:
        with self.lock:
            if not history.id:
                history.id = len(self.histories) + 1
            else:
                for i, h in enumerate(self.histories):
                    if h.id == history.id:
                        self.histories[i] = history
                        return history
            self.histories.append(history)
            return history

    def find_by_user_id(self, user_id: int) -> List[ListeningHistory]:
        with self.lock:
            return [h for h in self.histories if h.user_id == user_id]

    def find_by_user_id_and_song_id(self, user_id: int, song_id: str) -> List[ListeningHistory]:
        with self.lock:
            return [h for h in self.histories if h.user_id == user_id and h.song_id == song_id]
