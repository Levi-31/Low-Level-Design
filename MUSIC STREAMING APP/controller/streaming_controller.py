


from service.streaming_service import StreamingService


class StreamingController:
    def __init__(self, streaming_service: StreamingService):
        self.streaming_service = streaming_service

    def stream(self, song_id: str, start: int, end: int, user_id: int) -> bytes:
        # Validate user has access logic could be here
        return self.streaming_service.get_chunk(song_id, start, end)