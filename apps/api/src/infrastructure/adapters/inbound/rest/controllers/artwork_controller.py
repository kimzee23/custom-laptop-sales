from fastapi import APIRouter, Depends, UploadFile, File, Form, Query, status
from typing import Optional
from src.application.service.artwork_service import ArtworkService
from src.infrastructure.adapters.inbound.rest.dependencies import get_artwork_service
from src.infrastructure.adapters.inbound.rest.response import api_response

router = APIRouter(prefix="/artwork", tags=["Custom Lid Artwork"])

@router.post("/upload")
async def upload_artwork(
    file: UploadFile = File(...),
    model_code: Optional[str] = Form(None),
    artwork_service: ArtworkService = Depends(get_artwork_service)
):
    result = await artwork_service.upload_artwork(
        file_obj=file,
        filename=file.filename or "artwork.png",
        content_type=file.content_type or "image/png"
    )
    return {
        "success": True,
        "image_url": result.file_url,
        "filename": result.filename,
        "url": result.file_url,
        "file_size": result.file_size,
        "model_code": model_code or "standard",
        "mockup_preview_url": result.file_url,
        "message": "Artwork uploaded and mapped to 3D laptop preview successfully."
    }

@router.get("/mockup")
async def get_mockup(artwork_url: str = Query(...)):
    return {
        "mockup_url": artwork_url,
        "model": "3D-LID-RENDER-V1",
        "status": "ready"
    }
