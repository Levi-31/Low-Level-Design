



from dataclasses import dataclass, field
import time
from typing import Optional

from domain.download_status import DownloadStatus


@dataclass
class Download:
    id: int
    download_id: str
    user_id: int
    song_id: str
    device_id: str
    status: DownloadStatus = DownloadStatus.PENDING
    local_file_path: Optional[str] = None
    downloaded_at: int = 0
    created_at: int = field(default_factory=lambda: int(time.time()))