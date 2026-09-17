import os
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from app.schemas import ArtworkUploadResponse

router = APIRouter(prefix="/artwork", tags=["Custom Laser & Artwork"])

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "static", "uploads", "artwork")
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".svg", ".webp"}
MAX_FILE_SIZE = 15 * 1024 * 1024  # 15 MB

@router.post("/upload", response_model=ArtworkUploadResponse)
async def upload_artwork(
    file: UploadFile = File(...)
):
    """
    Upload customer artwork/logo/vector for high-precision UV or laser lid engraving.
    """
    file_ext = os.path.splitext(file.filename or "")[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file format '{file_ext}'. Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Read and validate size
    content = await file.read()
    file_size = len(content)
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Artwork file size exceeds maximum limit of 15MB"
        )

    # Save to disk
    unique_name = f"artwork_{uuid.uuid4().hex[:10]}{file_ext}"
    dest_path = os.path.join(UPLOAD_DIR, unique_name)
    with open(dest_path, "wb") as f:
        f.write(content)

    public_url = f"/static/uploads/artwork/{unique_name}"

    return ArtworkUploadResponse(
        success=True,
        image_url=public_url,
        filename=file.filename or unique_name,
        file_size=file_size,
        content_type=file.content_type or "image/png",
        message="Artwork uploaded and queued for precision engraving calibration"
    )
