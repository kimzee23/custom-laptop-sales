from abc import ABC, abstractmethod
from typing import BinaryIO
from src.domain.model.artwork import ArtworkUploadResult

class ArtworkStoragePort(ABC):
    @abstractmethod
    async def save_file(self, file_obj: BinaryIO, filename: str, content_type: str) -> ArtworkUploadResult:
        pass
