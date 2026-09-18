from fastapi import APIRouter, Depends, Header, Request, Query, status
from typing import Optional, Dict, Any
from src.domain.model.payment import PaymentProvider
from src.application.service.payment_service import PaymentService
from src.infrastructure.adapters.inbound.rest.dependencies import (
    get_payment_service, get_optional_user
)
from src.infrastructure.adapters.inbound.rest.dtos.schemas import (
    PaymentInitializeRequest, PaymentVerifyRequest
)
from src.infrastructure.adapters.inbound.rest.response import api_response

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/initialize")
async def initialize_payment(
    req: PaymentInitializeRequest,
    x_idempotency_key: Optional[str] = Header(None),
    user = Depends(get_optional_user),
    payment_service: PaymentService = Depends(get_payment_service)
):
    provider_str = req.provider.upper()
    provider = PaymentProvider(provider_str) if provider_str in PaymentProvider.__members__ else PaymentProvider.PAYSTACK
    key = req.idempotency_key or x_idempotency_key
    order_identifier = req.order_id or req.order_number

    result = await payment_service.initialize_payment(
        order_id=order_identifier,
        provider=provider,
        idempotency_key=key,
        user_id=user.id if user else None
    )
    return result

@router.post("/verify")
async def verify_payment(
    req: PaymentVerifyRequest,
    payment_service: PaymentService = Depends(get_payment_service)
):
    provider_str = req.provider.upper()
    provider = PaymentProvider(provider_str) if provider_str in PaymentProvider.__members__ else PaymentProvider.PAYSTACK
    result = await payment_service.verify_payment(reference=req.reference, provider=provider)
    return result

@router.post("/webhook")
async def handle_webhook(
    request: Request,
    provider: Optional[str] = Query("PAYSTACK"),
    x_paystack_signature: Optional[str] = Header(None),
    payment_service: PaymentService = Depends(get_payment_service)
):
    payload = await request.json()
    event_id = payload.get("id") or payload.get("event") or "webhook_event"
    event_type = payload.get("event", "charge.success")
    provider_enum = PaymentProvider(provider.upper()) if provider and provider.upper() in PaymentProvider.__members__ else PaymentProvider.PAYSTACK

    result = await payment_service.handle_webhook(
        provider=provider_enum,
        event_id=str(event_id),
        event_type=event_type,
        payload=payload
    )
    return result

@router.get("/gateways")
async def get_supported_gateways(payment_service: PaymentService = Depends(get_payment_service)):
    return payment_service.get_supported_gateways()
