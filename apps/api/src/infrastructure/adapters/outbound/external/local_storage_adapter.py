import os
import uuid
from typing import BinaryIO
from src.domain.model.artwork import ArtworkUploadResult
from src.application.ports.outbound.artwork_storage_port import ArtworkStoragePort

class LocalStorageAdapter(ArtworkStoragePort):
    def __init__(self, base_dir: str = None):
        if not base_dir:
            base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "static", "uploads", "artwork")
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    async def save_file(self, file_obj: BinaryIO, filename: str, content_type: str) -> ArtworkUploadResult:
        ext = filename.split(".")[-1] if "." in filename else "png"
        saved_name = f"artwork_{uuid.uuid4().hex[:10]}.{ext}"
        filepath = os.path.join(self.base_dir, saved_name)

        content = await file_obj.read()
        with open(filepath, "wb") as f:
            f.write(content)

        file_url = f"/static/uploads/artwork/{saved_name}"
        return ArtworkUploadResult(
            filename=saved_name,
            file_url=file_url,
            file_size=len(content),
            content_type=content_type
        )
