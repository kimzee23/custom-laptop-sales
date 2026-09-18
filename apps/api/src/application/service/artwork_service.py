from typing import BinaryIO
from src.domain.model.artwork import ArtworkUploadResult
from src.application.ports.inbound.artwork_usecase import ArtworkUseCase
from src.application.ports.outbound.artwork_storage_port import ArtworkStoragePort

class ArtworkService(ArtworkUseCase):
    def __init__(self, storage_port: ArtworkStoragePort):
        self.storage = storage_port

    async def upload_artwork(self, file_obj: BinaryIO, filename: str, content_type: str) -> ArtworkUploadResult:
        return await self.storage.save_file(file_obj, filename, content_type)
