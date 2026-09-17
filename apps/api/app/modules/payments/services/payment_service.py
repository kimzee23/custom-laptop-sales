import hashlib
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, Protocol
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.models import Payment, Order, ProcessedWebhookEvent
from app.modules.payments.domain.models import (
    PaymentRequest,
    PaymentInitializationResult,
    PaymentVerificationResult,
    ParsedWebhookEvent,
    PaymentCompletedEvent,
    PaymentStatus,
    PaymentProviderType
)
from app.modules.payments.domain.interfaces import PaymentProvider
from app.modules.payments.providers.factory import PaymentProviderFactory
from app.modules.payments.services.event_dispatcher import PaymentEventDispatcher
import app.modules.payments.services.order_fulfillment_service # ensure subscription

logger = logging.getLogger(__name__)

class PaymentService(Protocol):
    """
    High-level Application Payment Service interface.
    The controllers and business logic interact exclusively with this service.
    """
    async def initialize_payment(
        self,
        order_number: str,
        provider_type: PaymentProviderType,
        idempotency_key: str,
        db: AsyncSession,
        callback_url: Optional[str] = None
    ) -> Dict[str, Any]:
        ...

    async def verify_payment(
        self,
        provider_type: PaymentProviderType,
        reference: str,
        db: AsyncSession
    ) -> Dict[str, Any]:
        ...

    async def handle_webhook(
        self,
        provider_type: PaymentProviderType,
        raw_body: bytes,
        headers: Dict[str, str],
        payload: Dict[str, Any],
        db: AsyncSession
    ) -> Dict[str, Any]:
        ...


class PaymentServiceImpl:
    """
    Production-grade PaymentService implementation with:
    - Strict Idempotency guarantees & race condition protection
    - Provider abstraction (Paystack, Flutterwave, OPay)
    - Gateway timeout & retry safety
    - Idempotent Webhook processing
    - Decoupled Order Fulfillment via PaymentCompletedEvent
    """

    def __init__(self, provider_factory: Optional[PaymentProviderFactory] = None):
        self.provider_factory = provider_factory or PaymentProviderFactory

    async def initialize_payment(
        self,
        order_number: str,
        provider_type: PaymentProviderType,
        idempotency_key: str,
        db: AsyncSession,
        callback_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Idempotently initialize a payment for an order.
        If an initialization with the same idempotency key already exists, returns the existing record.
        Prevents double charging or multiple gateway authorizations.
        """
        if not idempotency_key or not idempotency_key.strip():
            raise ValueError("Idempotency-Key is required to initialize payment")

        idempotency_key = idempotency_key.strip()

        # 1. Check if a payment with this idempotency key already exists in DB
        stmt = select(Payment).where(Payment.idempotency_key == idempotency_key)
        result = await db.execute(stmt)
        existing_payment = result.scalar_one_or_none()

        if existing_payment:
            logger.info(f"Idempotency match found for key '{idempotency_key}'. Returning existing payment #{existing_payment.id}.")
            return {
                "payment_id": existing_payment.id,
                "order_number": order_number,
                "provider": PaymentProviderType(existing_payment.provider),
                "provider_reference": existing_payment.provider_reference,
                "access_code": existing_payment.access_code,
                "checkout_url": existing_payment.checkout_url or "",
                "amount": existing_payment.amount,
                "currency": existing_payment.currency,
                "status": PaymentStatus(existing_payment.status),
                "idempotent_replay": True,
                "created_at": existing_payment.created_at.isoformat() if existing_payment.created_at else datetime.utcnow().isoformat()
            }

        # 2. Fetch the target order
        order_stmt = select(Order).where(Order.order_number == order_number)
        order_res = await db.execute(order_stmt)
        order = order_res.scalar_one_or_none()
        if not order:
            raise ValueError(f"Order #{order_number} not found")

        # 3. Obtain provider adapter from factory
        provider: PaymentProvider = self.provider_factory.get_provider(provider_type)

        payment_req = PaymentRequest(
            order_id=order.id,
            order_number=order.order_number,
            amount=order.total_amount,
            currency=order.currency,
            customer_email=order.customer_email,
            customer_name=order.customer_name,
            customer_phone=order.customer_phone,
            callback_url=callback_url,
            idempotency_key=idempotency_key,
            metadata={"order_number": order.order_number}
        )

        # 4. Call provider to initialize checkout session
        try:
            init_result: PaymentInitializationResult = await provider.initialize(payment_req)
        except TimeoutError as te:
            logger.error(f"Gateway timeout while initializing payment: {te}")
            raise

        # 5. Persist the Payment record with DB unique constraint on idempotency_key
        new_payment = Payment(
            order_id=order.id,
            user_id=order.user_id,
            amount=order.total_amount,
            currency=order.currency,
            status=PaymentStatus.INITIATED.value,
            provider=provider_type.value,
            provider_reference=init_result.provider_reference,
            access_code=init_result.access_code,
            checkout_url=init_result.checkout_url,
            idempotency_key=idempotency_key,
            gateway_response=init_result.raw_response,
            created_at=datetime.utcnow()
        )

        db.add(new_payment)
        try:
            await db.commit()
            await db.refresh(new_payment)
        except IntegrityError:
            # Handle concurrent race condition: another request inserted with same key
            await db.rollback()
            retry_stmt = select(Payment).where(Payment.idempotency_key == idempotency_key)
            retry_res = await db.execute(retry_stmt)
            concurrent_payment = retry_res.scalar_one_or_none()
            if concurrent_payment:
                return {
                    "payment_id": concurrent_payment.id,
                    "order_number": order_number,
                    "provider": PaymentProviderType(concurrent_payment.provider),
                    "provider_reference": concurrent_payment.provider_reference,
                    "access_code": concurrent_payment.access_code,
                    "checkout_url": concurrent_payment.checkout_url or "",
                    "amount": concurrent_payment.amount,
                    "currency": concurrent_payment.currency,
                    "status": PaymentStatus(concurrent_payment.status),
                    "idempotent_replay": True,
                    "created_at": concurrent_payment.created_at.isoformat() if concurrent_payment.created_at else datetime.utcnow().isoformat()
                }
            raise

        return {
            "payment_id": new_payment.id,
            "order_number": order.order_number,
            "provider": provider_type,
            "provider_reference": new_payment.provider_reference,
            "access_code": new_payment.access_code,
            "checkout_url": new_payment.checkout_url,
            "amount": new_payment.amount,
            "currency": new_payment.currency,
            "status": PaymentStatus(new_payment.status),
            "idempotent_replay": False,
            "created_at": new_payment.created_at.isoformat()
        }

    async def verify_payment(
        self,
        provider_type: PaymentProviderType,
        reference: str,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """
        Verify payment state with provider.
        - If already verified SUCCESS, returns immediately without re-triggering fulfillment.
        - If in INITIATED/PROCESSING, calls gateway and transitions state.
        - If SUCCESS, dispatches PaymentCompletedEvent to fulfill order.
        """
        stmt = select(Payment).where(Payment.provider_reference == reference)
        res = await db.execute(stmt)
        payment = res.scalar_one_or_none()

        # If payment record is already in SUCCESS state, return verified state
        if payment and payment.status == PaymentStatus.SUCCESS.value:
            order_stmt = select(Order).where(Order.id == payment.order_id)
            order_res = await db.execute(order_stmt)
            order = order_res.scalar_one_or_none()
            return {
                "payment_id": payment.id,
                "order_number": order.order_number if order else "UNKNOWN",
                "provider": provider_type,
                "provider_reference": payment.provider_reference,
                "status": PaymentStatus.SUCCESS,
                "amount": payment.amount,
                "currency": payment.currency,
                "channel": payment.channel,
                "paid_at": payment.paid_at.isoformat() if payment.paid_at else None,
                "gateway_message": "Payment already verified successfully",
                "order_status": order.status if order else "PAID"
            }

        provider: PaymentProvider = self.provider_factory.get_provider(provider_type)
        verify_res: PaymentVerificationResult = await provider.verify(reference)

        if payment:
            payment.status = verify_res.status.value
            payment.channel = verify_res.channel or payment.channel
            payment.gateway_response = verify_res.raw_response
            if verify_res.status == PaymentStatus.SUCCESS:
                payment.paid_at = verify_res.paid_at or datetime.utcnow()
            elif verify_res.status == PaymentStatus.FAILED:
                payment.failure_reason = verify_res.gateway_message
            await db.commit()

            # If successful, publish decoupled event
            if verify_res.status == PaymentStatus.SUCCESS:
                order_stmt = select(Order).where(Order.id == payment.order_id)
                order_res = await db.execute(order_stmt)
                order = order_res.scalar_one_or_none()

                if order:
                    event = PaymentCompletedEvent(
                        payment_id=payment.id,
                        order_id=order.id,
                        order_number=order.order_number,
                        provider=provider_type,
                        provider_reference=reference,
                        amount=payment.amount,
                        currency=payment.currency,
                        customer_email=order.customer_email,
                        customer_name=order.customer_name,
                        completed_at=payment.paid_at or datetime.utcnow()
                    )
                    await PaymentEventDispatcher.publish_payment_completed(event, db=db)

            order_status = "PAID" if verify_res.status == PaymentStatus.SUCCESS else "PENDING_PAYMENT"
            return {
                "payment_id": payment.id,
                "order_number": order.order_number if 'order' in locals() and order else "UNKNOWN",
                "provider": provider_type,
                "provider_reference": reference,
                "status": verify_res.status,
                "amount": verify_res.amount or payment.amount,
                "currency": verify_res.currency or payment.currency,
                "channel": verify_res.channel,
                "paid_at": payment.paid_at.isoformat() if payment.paid_at else None,
                "gateway_message": verify_res.gateway_message,
                "order_status": order_status
            }

        # Fallback when payment was initialized externally
        return {
            "payment_id": "N/A",
            "order_number": "N/A",
            "provider": provider_type,
            "provider_reference": reference,
            "status": verify_res.status,
            "amount": verify_res.amount,
            "currency": verify_res.currency,
            "channel": verify_res.channel,
            "paid_at": verify_res.paid_at.isoformat() if verify_res.paid_at else None,
            "gateway_message": verify_res.gateway_message,
            "order_status": "UNKNOWN"
        }

    async def handle_webhook(
        self,
        provider_type: PaymentProviderType,
        raw_body: bytes,
        headers: Dict[str, str],
        payload: Dict[str, Any],
        db: AsyncSession
    ) -> Dict[str, Any]:
        """
        Idempotent Webhook processor:
        1. Validates cryptographic signature.
        2. Validates uniqueness of event_id in ProcessedWebhookEvent table.
        3. If already processed: gracefully returns without re-triggering side-effects.
        4. If new: updates Payment status and publishes PaymentCompletedEvent.
        """
        provider: PaymentProvider = self.provider_factory.get_provider(provider_type)

        # 1. Signature Verification
        if not provider.verify_webhook_signature(raw_body, headers):
            logger.warning(f"Invalid webhook signature received for provider {provider_type}")
            raise PermissionError(f"Invalid {provider_type} webhook signature")

        # 2. Parse standardized event
        parsed_event: ParsedWebhookEvent = provider.parse_webhook(payload)

        # 3. Check Webhook Idempotency
        evt_stmt = select(ProcessedWebhookEvent).where(
            ProcessedWebhookEvent.event_id == parsed_event.event_id
        )
        evt_res = await db.execute(evt_stmt)
        if evt_res.scalar_one_or_none():
            logger.info(f"Duplicate webhook event '{parsed_event.event_id}' for {provider_type}. Safely ignoring.")
            return {"status": "ignored", "message": "Event already processed", "event_id": parsed_event.event_id}

        # 4. Record the processed webhook event
        payload_hash = hashlib.sha256(raw_body).hexdigest()
        webhook_record = ProcessedWebhookEvent(
            provider=provider_type.value,
            event_id=parsed_event.event_id,
            event_type=parsed_event.event_type,
            payload_hash=payload_hash,
            raw_payload=payload,
            processed_at=datetime.utcnow()
        )
        db.add(webhook_record)

        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            logger.info(f"Concurrent duplicate webhook event '{parsed_event.event_id}' detected. Skipping.")
            return {"status": "ignored", "message": "Event already processed concurrently", "event_id": parsed_event.event_id}

        # 5. Find matching payment & update state
        pay_stmt = select(Payment).where(Payment.provider_reference == parsed_event.provider_reference)
        pay_res = await db.execute(pay_stmt)
        payment = pay_res.scalar_one_or_none()

        if payment:
            payment.status = parsed_event.status.value
            if parsed_event.status == PaymentStatus.SUCCESS:
                payment.paid_at = parsed_event.paid_at or datetime.utcnow()
            await db.commit()

            # Publish event if successful
            if parsed_event.status == PaymentStatus.SUCCESS:
                order_stmt = select(Order).where(Order.id == payment.order_id)
                order_res = await db.execute(order_stmt)
                order = order_res.scalar_one_or_none()
                if order:
                    event = PaymentCompletedEvent(
                        payment_id=payment.id,
                        order_id=order.id,
                        order_number=order.order_number,
                        provider=provider_type,
                        provider_reference=parsed_event.provider_reference,
                        amount=parsed_event.amount or payment.amount,
                        currency=parsed_event.currency or payment.currency,
                        customer_email=order.customer_email,
                        customer_name=order.customer_name,
                        completed_at=payment.paid_at or datetime.utcnow()
                    )
                    await PaymentEventDispatcher.publish_payment_completed(event, db=db)

        return {
            "status": "success",
            "message": "Webhook processed successfully",
            "event_id": parsed_event.event_id,
            "provider_reference": parsed_event.provider_reference
        }

payment_service = PaymentServiceImpl()
