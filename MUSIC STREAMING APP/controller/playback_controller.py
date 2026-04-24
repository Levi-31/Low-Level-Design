



from domain.playback_source import PlaybackSource
from domain.repeat_mode import RepeatMode
from service.playback_service import PlaybackService, PlaybackStateResponse


class PlaybackController:
    def __init__(self, playback_service: PlaybackService):
        self.playback_service = playback_service

    def play(self, user_id: int, source_type: PlaybackSource, source_id: str, start_position: int) -> PlaybackStateResponse:
        return self.playback_service.play(user_id, source_type, source_id, start_position)

    def pause(self, session_id: str) -> PlaybackStateResponse:
        return self.playback_service.pause(session_id)

    def resume(self, session_id: str) -> PlaybackStateResponse:
        return self.playback_service.resume(session_id)

    def skip_next(self, session_id: str) -> PlaybackStateResponse:
        return self.playback_service.skip_next(session_id)

    def skip_previous(self, session_id: str) -> PlaybackStateResponse:
        # Assuming skip_previous is implemented in service
        return self.playback_service.skip_previous(session_id)

    def get_state(self, session_id: str) -> PlaybackStateResponse:
        return self.playback_service.get_state(session_id)

    def toggle_shuffle(self, session_id: str, enabled: bool) -> PlaybackStateResponse:
        return self.playback_service.toggle_shuffle(session_id, enabled)

    def set_repeat_mode(self, session_id: str, mode: RepeatMode) -> PlaybackStateResponse:
        return self.playback_service.set_repeat_mode(session_id, mode)

    def update_position(self, session_id: str, position: int) -> None:
        self.playback_service.update_position(session_id, position)
