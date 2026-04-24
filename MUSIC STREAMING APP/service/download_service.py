



import time
from typing import Optional , List

from domain.download import Download
from domain.download_status import DownloadStatus
from domain.subscription_tier import SubscriptionTier
from repository.repository_interfaces import DownloadRepository , UserRepository


class DownloadService:
    MAX_DEVICES = 5
    MAX_DOWNLOADS = 10000

    def __init__(self, download_repo: DownloadRepository, user_repo: UserRepository):
        self.download_repo = download_repo
        self.user_repo = user_repo

    def _validate_device_limit(self, user_id: int, device_id: str) -> bool:
        downloads = self.download_repo.find_by_user_id(user_id)
        devices = {d.device_id for d in downloads}
        
        device_downloads = self.download_repo.find_by_user_id_and_device_id(user_id, device_id)
        if len(device_downloads) > 0:
            return True
            
        return len(devices) < self.MAX_DEVICES
    
    def download_song(self, user_id: int, song_id: str, device_id: str) -> Download:
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise ValueError(f"User not found: {user_id}")
            
        if user.subscription_tier != SubscriptionTier.PREMIUM:
            raise ValueError("Premium subscription required for downloads")
            
        if not self._validate_device_limit(user_id, device_id):
            raise ValueError(f"Device limit exceeded. Max {self.MAX_DEVICES} devices allowed")
            
        user_downloads = self.download_repo.find_by_user_id(user_id)
        if len(user_downloads) >= self.MAX_DOWNLOADS:
            raise ValueError(f"Download limit exceeded. Max {self.MAX_DOWNLOADS} songs allowed")
            
        now = int(time.time())
        download_id = f"DL_{now}_{song_id}"
        
        download = Download(
            id=0,
            download_id=download_id,
            user_id=user_id,
            song_id=song_id,
            device_id=device_id,
            status=DownloadStatus.COMPLETED,
            local_file_path=f"/cache/{device_id}/{song_id}",
            downloaded_at=now,
            created_at=now
        )
        
        return self.download_repo.save(download)
    
    def get_downloads(self, user_id: int, device_id: Optional[str] = None) -> List[Download]:
        if device_id:
            return self.download_repo.find_by_user_id_and_device_id(user_id, device_id)
        return self.download_repo.find_by_user_id(user_id)

    def delete_download(self, download_id: str, user_id: int) -> None:
        self.download_repo.remove(download_id)