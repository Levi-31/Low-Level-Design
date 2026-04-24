



import time
from typing import List, Optional

from domain.listening_history import ListeningHistory
from domain.playback_session import PlaybackSession
from domain.playback_source import PlaybackSource
from domain.playback_status import PlaybackStatus
from domain.repeat_mode import RepeatMode
from domain.song import Song
from repository.repository_interfaces import AlbumRepository, ListeningHistoryRepository, PlaybackSessionRepository, PlaylistRepository, SongRepository, UserRepository
from service.streaming_service import StreamingService


class PlaybackStateResponse:
    def __init__(self):
        self.session_id: str = ""
        self.current_song: Optional[Song] = None
        self.current_position: int = 0
        self.queue: List[Song] = []
        self.shuffle_mode: bool = False
        self.repeat_mode: RepeatMode = RepeatMode.OFF
        self.status: PlaybackStatus = PlaybackStatus.STOPPED
        self.stream_url: str = ""

class PlaybackService:
    COMPLETION_THRESHOLD = 0.9

    def __init__(self, 
                 session_repo: PlaybackSessionRepository,
                 song_repo: SongRepository,
                 album_repo: AlbumRepository,
                 playlist_repo: PlaylistRepository,
                 user_repo: UserRepository,
                 history_repo: ListeningHistoryRepository,
                 streaming_service: StreamingService):
        self.session_repo = session_repo
        self.song_repo = song_repo
        self.album_repo = album_repo
        self.playlist_repo = playlist_repo
        self.user_repo = user_repo
        self.history_repo = history_repo
        self.streaming_service = streaming_service

    def _get_session(self, session_id: str) -> PlaybackSession:
        session = self.session_repo.find_by_id(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        return session
    
    def _build_queue(self, source_type: PlaybackSource, source_id: str) -> List[str]:
        if source_type == PlaybackSource.SONG:
            return [source_id]
        elif source_type == PlaybackSource.ALBUM:
            album = self.album_repo.find_by_id(source_id)
            if not album:
                return []
            songs = self.song_repo.find_by_album_id(source_id)
            return [s.song_id for s in songs]
        elif source_type == PlaybackSource.PLAYLIST:
            playlist = self.playlist_repo.find_by_id(source_id)
            if not playlist:
                return []
            return list(playlist.song_ids)
        return []
    
    def _save_listening_history(self, user_id: int, song_id: str, play_duration: int, completed: bool):
        now = int(time.time())
        history = ListeningHistory(
            id=0,
            user_id=user_id,
            song_id=song_id,
            play_duration=play_duration,
            completed=completed,
            played_at=now
        )
        self.history_repo.save(history)


    def _build_playback_state_response(self, session: PlaybackSession, stream_url: str) -> PlaybackStateResponse:
        response = PlaybackStateResponse()
        response.session_id = session.session_id
        response.current_song = self.song_repo.find_by_id(session.current_song_id)
        response.current_position = session.current_position
        
        for sid in session.queue:
            s = self.song_repo.find_by_id(sid)
            if s:
                response.queue.append(s)
                
        response.shuffle_mode = session.shuffle_mode
        response.repeat_mode = session.repeat_mode
        response.status = session.status
        response.stream_url = stream_url
        return response
    

    def play(self, user_id: int, source_type: PlaybackSource, source_id: str, start_position: int) -> PlaybackStateResponse:
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise ValueError(f"User not found: {user_id}")
            
        queue = self._build_queue(source_type, source_id)
        if not queue:
            raise ValueError(f"No songs found for source: {source_id}")
            
        current_song_id = queue[0]
        device_id = f"device_{user_id}"
        
        existing_session = self.session_repo.find_by_user_id_and_device_id(user_id, device_id)
        
        if existing_session:
            session = existing_session
            session.current_song_id = current_song_id
            session.current_position = start_position
            session.queue = queue
            session.source = source_type
            session.source_id = source_id
            session.status = PlaybackStatus.PLAYING
            session.last_updated_at = int(time.time())
        else:
            now = int(time.time())
            session_id = f"SESS_{now}"
            session = PlaybackSession(
                id=0,
                session_id=session_id,
                user_id=user_id,
                device_id=device_id,
                current_song_id=current_song_id,
                current_position=start_position,
                source=source_type,
                source_id=source_id,
                queue=queue,
                status=PlaybackStatus.PLAYING,
                started_at=now,
                last_updated_at=now
            )
            
        session = self.session_repo.save(session)
        stream_url = self.streaming_service.get_stream_url(current_song_id, user_id)
        return self._build_playback_state_response(session, stream_url)
    
    def pause(self, session_id: str) -> PlaybackStateResponse:
        session = self._get_session(session_id)
        session.status = PlaybackStatus.PAUSED
        session.last_updated_at = int(time.time())
        session = self.session_repo.save(session)
        return self._build_playback_state_response(session, "")
    

    def resume(self, session_id: str) -> PlaybackStateResponse:
        session = self._get_session(session_id)
        session.status = PlaybackStatus.PLAYING
        session.last_updated_at = int(time.time())
        session = self.session_repo.save(session)
        return self._build_playback_state_response(session, "")
    
    def skip_next(self, session_id: str) -> PlaybackStateResponse:
        session = self._get_session(session_id)
        
        self._save_listening_history(session.user_id, session.current_song_id, session.current_position, False)
        
        next_song_id = ""
        if session.current_song_id in session.queue:
            idx = session.queue.index(session.current_song_id)
            if session.repeat_mode == RepeatMode.ONE:
                next_song_id = session.current_song_id
            elif idx + 1 < len(session.queue):
                next_song_id = session.queue[idx + 1]
                
        if not next_song_id:
            session.status = PlaybackStatus.STOPPED
        else:
            session.current_song_id = next_song_id
            session.current_position = 0
            
        session.last_updated_at = int(time.time())
        session = self.session_repo.save(session)
        
        stream_url = "" if not next_song_id else self.streaming_service.get_stream_url(next_song_id, session.user_id)
        return self._build_playback_state_response(session, stream_url)
    
    def skip_previous(self, session_id: str) -> PlaybackStateResponse:
        session = self._get_session(session_id)
        
        prev_song_id = ""
        if session.current_song_id in session.queue:
            idx = session.queue.index(session.current_song_id)
            if idx > 0:
                prev_song_id = session.queue[idx - 1]
                
        if prev_song_id:
            session.current_song_id = prev_song_id
            session.current_position = 0
            
        session.last_updated_at = int(time.time())
        session = self.session_repo.save(session)
        
        stream_url = "" if not prev_song_id else self.streaming_service.get_stream_url(prev_song_id, session.user_id)
        return self._build_playback_state_response(session, stream_url)
    

    def get_state(self, session_id: str) -> PlaybackStateResponse:
        session = self._get_session(session_id)
        return self._build_playback_state_response(session, "")
    

    def toggle_shuffle(self, session_id: str, enabled: bool) -> PlaybackStateResponse:
        session = self._get_session(session_id)
        session.shuffle_mode = enabled
        session.last_updated_at = int(time.time())
        session = self.session_repo.save(session)
        return self._build_playback_state_response(session, "")
    

    def set_repeat_mode(self, session_id: str, mode: RepeatMode) -> PlaybackStateResponse:
        session = self._get_session(session_id)
        session.repeat_mode = mode
        session.last_updated_at = int(time.time())
        session = self.session_repo.save(session)
        return self._build_playback_state_response(session, "")

    def update_position(self, session_id: str, position: int) -> None:
        session = self._get_session(session_id)
        session.current_position = position
        session.last_updated_at = int(time.time())
        self.session_repo.save(session)
        
        song = self.song_repo.find_by_id(session.current_song_id)
        if song:
            completed = position >= (song.duration * self.COMPLETION_THRESHOLD)
            self._save_listening_history(session.user_id, session.current_song_id, position, completed)
