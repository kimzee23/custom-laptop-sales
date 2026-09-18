from dataclasses import dataclass
from typing import Optional

@dataclass
class ArtworkUploadResult:
    filename: str
    file_url: str
    file_size: int
    content_type: str
