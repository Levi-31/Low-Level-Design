

from typing import List, Optional

from domain.download import Download
from service.download_service import DownloadService


class DownloadController:
    def __init__(self, download_service: DownloadService):
        self.download_service = download_service

    def download(self, user_id: int, song_id: str, device_id: str) -> Download:
        return self.download_service.download_song(user_id, song_id, device_id)

    def get_downloads(self, user_id: int, device_id: Optional[str] = None) -> List[Download]:
        return self.download_service.get_downloads(user_id, device_id)

    def delete_download(self, download_id: str, user_id: int) -> None:
        self.download_service.delete_download(download_id, user_id)