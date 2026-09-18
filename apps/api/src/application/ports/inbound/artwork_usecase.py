from abc import ABC, abstractmethod
from typing import BinaryIO
from src.domain.model.artwork import ArtworkUploadResult

class ArtworkUseCase(ABC):
    @abstractmethod
    async def upload_artwork(self, file_obj: BinaryIO, filename: str, content_type: str) -> ArtworkUploadResult:
        pass
