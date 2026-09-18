from fastapi import APIRouter, Depends, Query, status
from typing import Optional, List
from src.application.service.configuration_service import ConfigurationService
from src.infrastructure.adapters.inbound.rest.dependencies import (
    get_configuration_service, get_optional_user, get_current_user
)
from src.infrastructure.adapters.inbound.rest.dtos.schemas import (
    PriceCalculationRequest, ConfigurationSubmitRequest, SaveBuildRequest
)
from src.infrastructure.adapters.inbound.rest.response import api_response

router = APIRouter(tags=["Laptop Configuration"])

@router.post("/configurations/price")
async def calculate_price(
    req: PriceCalculationRequest,
    config_service: ConfigurationService = Depends(get_configuration_service)
):
    opt_ids = [
        req.color_id, req.ram_id, req.storage_id, req.cpu_id, req.gpu_id,
        req.display_id, req.keyboard_id
    ]
    if req.accessory_ids:
        opt_ids.extend(req.accessory_ids)
    if req.selected_option_ids:
        opt_ids.extend(req.selected_option_ids)
    opt_ids = [o for o in opt_ids if o]

    result = await config_service.calculate_price(
        product_id=req.product_id,
        base_price=req.base_price,
        selected_option_ids=opt_ids,
        artwork=req.artwork
    )
    return result

@router.post("/configurations")
async def submit_configuration(
    req: ConfigurationSubmitRequest,
    config_service: ConfigurationService = Depends(get_configuration_service),
    user = Depends(get_optional_user)
):
    opt_ids = [
        req.color_id, req.ram_id, req.storage_id, req.cpu_id, req.gpu_id,
        req.display_id, req.keyboard_id
    ]
    if req.accessory_ids:
        opt_ids.extend(req.accessory_ids)
    opt_ids = [o for o in opt_ids if o]

    calc = await config_service.calculate_price(
        product_id=req.product_id,
        base_price=req.base_price,
        selected_option_ids=opt_ids,
        artwork=req.artwork
    )
    specs_summary = {
        "color": req.color_id,
        "ram": req.ram_id,
        "storage": req.storage_id,
        "cpu": req.cpu_id,
        "gpu": req.gpu_id,
        "display": req.display_id,
        "keyboard": req.keyboard_id,
        "accessories": req.accessory_ids,
        "has_artwork": bool(req.artwork and (req.artwork.get("image_url") or req.artwork.get("custom_text")))
    }
    return {
        "product_id": req.product_id,
        "product_title": calc["product_title"],
        "base_price": calc["base_price"],
        "total_price": calc["total"],
        "specs_summary": specs_summary,
        "applied_modifiers": calc["modifiers_total"],
        "items": calc["items"]
    }

@router.post("/saved-builds")
async def save_build(
    req: SaveBuildRequest,
    user = Depends(get_optional_user),
    config_service: ConfigurationService = Depends(get_configuration_service)
):
    uid = (user.id if user else None) or req.user_id or "guest-user"
    saved = await config_service.save_user_configuration(
        user_id=uid,
        title=req.title,
        product_id=req.product_id,
        image_url=req.image_url,
        total_price=req.total_price,
        configuration_snapshot=req.configuration_snapshot,
        specs_summary=req.specs_summary
    )
    return {
        "id": saved.id,
        "title": saved.title,
        "product_id": saved.product_id,
        "image_url": saved.image_url,
        "total_price": saved.total_price,
        "specs_summary": saved.specs_summary,
        "created_at": saved.created_at.isoformat() if saved.created_at else None
    }

@router.get("/saved-builds")
async def get_saved_builds(
    user_id: Optional[str] = Query(None),
    user = Depends(get_optional_user),
    config_service: ConfigurationService = Depends(get_configuration_service)
):
    uid = user_id or (user.id if user else None)
    builds = await config_service.get_saved_configurations(user_id=uid)
    return [
        {
            "id": b.id,
            "title": b.title,
            "product_id": b.product_id,
            "image_url": b.image_url,
            "total_price": b.total_price,
            "specs_summary": b.specs_summary,
            "configuration_snapshot": b.configuration_snapshot,
            "created_at": b.created_at.isoformat() if b.created_at else None
        }
        for b in builds
    ]
