import json
import logging
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Header, Request, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models import Payment, Order
from app.schemas import (
    PaymentGatewayInfo,
    PaymentProviderEnum,
    PaymentStatusEnum,
    PaymentInitializeRequest,
    PaymentInitializeResponse,
    PaymentVerificationResponse
)
from app.modules.payments.domain.models import PaymentProviderType, PaymentStatus
from app.modules.payments.services.payment_service import payment_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.get("/gateways", response_model=List[PaymentGatewayInfo])
async def list_payment_gateways():
    """
    Returns available Nigerian & international payment gateway providers.
    """
    return [
        PaymentGatewayInfo(
            id="paystack",
            name="Paystack Checkout",
            code=PaymentProviderEnum.PAYSTACK,
            description="Cards (Mastercard, Visa, Verve), Bank Transfer, USSD, Apple Pay",
            logo_icon="/images/paystack-logo.svg",
            supported_channels=["card", "bank_transfer", "ussd", "apple_pay", "qr"],
            badge="Instant Activation"
        ),
        PaymentGatewayInfo(
            id="flutterwave",
            name="Flutterwave Standard",
            code=PaymentProviderEnum.FLUTTERWAVE,
            description="Debit/Credit Cards, Mobile Money, Barter, USSD, Direct Bank Debit",
            logo_icon="/images/flutterwave-logo.svg",
            supported_channels=["card", "bank_transfer", "ussd", "mobile_money", "barter"],
            badge="Pan-African"
        ),
        PaymentGatewayInfo(
            id="opay",
            name="OPay Digital Services",
            code=PaymentProviderEnum.OPAY,
            description="OPay Wallet, Quick QR Scan, OPay Cards, Bank Transfer",
            logo_icon="/images/opay-logo.svg",
            supported_channels=["opay_wallet", "qr", "card", "bank_transfer"],
            badge="Zero Transfer Fees"
        )
    ]

@router.post("/initialize", response_model=PaymentInitializeResponse)
async def initialize_payment(
    body: PaymentInitializeRequest,
    idempotency_key_header: Optional[str] = Header(None, alias="Idempotency-Key"),
    db: AsyncSession = Depends(get_db)
):
    """
    Idempotent payment initialization endpoint.
    Accepts Idempotency-Key header or body field.
    Prevents duplicate payment records and duplicate gateway initialization calls.
    """
    effective_idempotency_key = (idempotency_key_header or body.idempotency_key or "").strip()
    if not effective_idempotency_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Idempotency key is required via 'Idempotency-Key' header or request body"
        )

    try:
        provider_type = PaymentProviderType(body.provider.value)
        result = await payment_service.initialize_payment(
            order_number=body.order_number,
            provider_type=provider_type,
            idempotency_key=effective_idempotency_key,
            callback_url=body.callback_url,
            db=db
        )
        return PaymentInitializeResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except TimeoutError as te:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=str(te))
    except Exception as exc:
        logger.error(f"Error initializing payment: {exc}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

@router.get("/verify/{provider}/{reference}", response_model=PaymentVerificationResponse)
async def verify_payment(
    provider: PaymentProviderEnum,
    reference: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Authoritative server-side payment verification endpoint.
    Validates transaction status with the provider and fulfills the associated order.
    """
    try:
        provider_type = PaymentProviderType(provider.value)
        result = await payment_service.verify_payment(
            provider_type=provider_type,
            reference=reference,
            db=db
        )
        return PaymentVerificationResponse(**result)
    except TimeoutError as te:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=str(te))
    except Exception as exc:
        logger.error(f"Error verifying payment: {exc}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

@router.get("/order/{order_number}/status")
async def get_order_payment_status(
    order_number: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Queries real-time payment and build status for an order.
    """
    stmt = select(Order).where(Order.order_number == order_number)
    res = await db.execute(stmt)
    order = res.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    pay_stmt = select(Payment).where(Payment.order_id == order.id).order_by(Payment.created_at.desc())
    pay_res = await db.execute(pay_stmt)
    payments = pay_res.scalars().all()

    return {
        "order_number": order.order_number,
        "order_status": order.status,
        "total_amount": order.total_amount,
        "currency": order.currency,
        "payment_gateway": order.payment_gateway,
        "payment_reference": order.payment_reference,
        "paid_at": order.paid_at.isoformat() if order.paid_at else None,
        "payments": [
            {
                "id": p.id,
                "provider": p.provider,
                "provider_reference": p.provider_reference,
                "status": p.status,
                "amount": p.amount,
                "created_at": p.created_at.isoformat() if p.created_at else None
            }
            for p in payments
        ]
    }

# -----------------
# Webhook Handlers
# -----------------

@router.post("/webhooks/paystack")
async def paystack_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Paystack Webhook Endpoint with HMAC-SHA512 verification and idempotency protection.
    """
    raw_body = await request.body()
    headers = dict(request.headers)
    try:
        payload = json.loads(raw_body.decode("utf-8")) if raw_body else {}
        result = await payment_service.handle_webhook(
            provider_type=PaymentProviderType.PAYSTACK,
            raw_body=raw_body,
            headers=headers,
            payload=payload,
            db=db
        )
        return result
    except PermissionError as pe:
        logger.warning(f"Paystack webhook unauthorized: {pe}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(pe))
    except Exception as exc:
        logger.error(f"Paystack webhook error: {exc}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

@router.post("/webhooks/flutterwave")
async def flutterwave_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Flutterwave Webhook Endpoint with secret hash verification and idempotency protection.
    """
    raw_body = await request.body()
    headers = dict(request.headers)
    try:
        payload = json.loads(raw_body.decode("utf-8")) if raw_body else {}
        result = await payment_service.handle_webhook(
            provider_type=PaymentProviderType.FLUTTERWAVE,
            raw_body=raw_body,
            headers=headers,
            payload=payload,
            db=db
        )
        return result
    except PermissionError as pe:
        logger.warning(f"Flutterwave webhook unauthorized: {pe}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(pe))
    except Exception as exc:
        logger.error(f"Flutterwave webhook error: {exc}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

@router.post("/webhooks/opay")
async def opay_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    OPay Webhook Endpoint with HMAC signature verification and idempotency protection.
    """
    raw_body = await request.body()
    headers = dict(request.headers)
    try:
        payload = json.loads(raw_body.decode("utf-8")) if raw_body else {}
        result = await payment_service.handle_webhook(
            provider_type=PaymentProviderType.OPAY,
            raw_body=raw_body,
            headers=headers,
            payload=payload,
            db=db
        )
        return result
    except PermissionError as pe:
        logger.warning(f"OPay webhook unauthorized: {pe}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(pe))
    except Exception as exc:
        logger.error(f"OPay webhook error: {exc}", exc_info=True)
@router.post("/webhook")
async def unified_webhook(
    request: Request,
    provider: Optional[str] = Query(None, description="Optional provider override: paystack, flutterwave, opay"),
    db: AsyncSession = Depends(get_db)
):
    """
    Unified webhook endpoint that automatically detects provider from signature headers or payload.
    """
    headers = dict(request.headers)
    raw_body = await request.body()
    payload = json.loads(raw_body.decode("utf-8")) if raw_body else {}

    # Auto-detect provider
    target_provider = PaymentProviderType.PAYSTACK
    if provider:
        p_lower = provider.lower()
        if "flutter" in p_lower:
            target_provider = PaymentProviderType.FLUTTERWAVE
        elif "opay" in p_lower:
            target_provider = PaymentProviderType.OPAY
    elif "x-paystack-signature" in headers:
        target_provider = PaymentProviderType.PAYSTACK
    elif "verif-hash" in headers or "flutterwave" in str(headers).lower():
        target_provider = PaymentProviderType.FLUTTERWAVE
    elif "authorization" in headers and "opay" in str(headers).lower():
        target_provider = PaymentProviderType.OPAY

    try:
        return await payment_service.handle_webhook(
            provider_type=target_provider,
            raw_body=raw_body,
            headers=headers,
            payload=payload,
            db=db
        )
    except PermissionError as pe:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(pe))
    except Exception as exc:
        logger.error(f"Unified webhook error: {exc}", exc_info=True)
        return {"status": "accepted", "message": "Webhook processed or safely acknowledged"}

@router.post("/mock-complete/{reference}")
async def mock_complete_payment(
    reference: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Development test helper endpoint to instantly simulate gateway payment success for a reference.
    """
    stmt = select(Payment).where(Payment.provider_reference == reference)
    res = await db.execute(stmt)
    payment = res.scalar_one_or_none()
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment reference not found")

    provider_type = PaymentProviderType(payment.provider)
    return await payment_service.verify_payment(provider_type=provider_type, reference=reference, db=db)
