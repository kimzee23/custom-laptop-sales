import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from src.domain.model.payment import Payment, PaymentStatus, PaymentProvider, ProcessedWebhookEvent
from src.domain.model.order import OrderStatus
from src.domain.exception.exceptions import (
    PaymentNotFoundException,
    OrderNotFoundException,
    DuplicateTransactionException
)
from src.application.ports.inbound.payment_usecase import PaymentUseCase
from src.application.ports.inbound.notification_usecase import NotificationUseCase
from src.application.ports.outbound.payment_repository_port import PaymentRepositoryPort
from src.application.ports.outbound.order_repository_port import OrderRepositoryPort
from src.application.ports.outbound.payment_gateway_port import PaymentGatewayPort

class PaymentService(PaymentUseCase):
    def __init__(
        self,
        payment_repository: PaymentRepositoryPort,
        order_repository: OrderRepositoryPort,
        gateway_adapters: Dict[PaymentProvider, PaymentGatewayPort],
        company_bank_details: Dict[str, str],
        notification_service: Optional[NotificationUseCase] = None
    ):
        self.payment_repo = payment_repository
        self.order_repo = order_repository
        self.gateways = gateway_adapters
        self.bank_details = company_bank_details
        self.notification_service = notification_service

    async def initialize_payment(
        self,
        order_id: str,
        provider: PaymentProvider,
        idempotency_key: str,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        # 1. Check idempotency
        existing_payment = await self.payment_repo.get_by_idempotency_key(idempotency_key)
        if existing_payment:
            return {
                "payment_id": existing_payment.id,
                "order_id": existing_payment.order_id,
                "reference": existing_payment.provider_reference,
                "provider_reference": existing_payment.provider_reference,
                "status": existing_payment.status.value,
                "amount": existing_payment.amount,
                "currency": existing_payment.currency,
                "checkout_url": existing_payment.checkout_url,
                "access_code": existing_payment.access_code,
                "is_idempotent_replay": True
            }

        # 2. Retrieve Order
        order = await self.order_repo.get_by_id(order_id)
        if not order:
            order = await self.order_repo.get_by_order_number(order_id)
        if not order:
            raise OrderNotFoundException(f"Order '{order_id}' not found.")

        # 3. Call Gateway
        gateway = self.gateways.get(provider)
        if not gateway:
            raise ValueError(f"Gateway for provider {provider} is not configured.")

        gateway_res = await gateway.initialize_transaction(
            order_id=order.order_number,
            amount=order.total_amount,
            email=order.customer_email,
            metadata={"order_id": order.id, "user_id": user_id, "customer_name": order.customer_name}
        )

        payment = Payment(
            id=str(uuid.uuid4()),
            order_id=order.id,
            user_id=user_id,
            amount=order.total_amount,
            currency=order.currency,
            status=PaymentStatus.INITIATED,
            provider=provider,
            provider_reference=gateway_res.get("reference", f"{provider.value.lower()}_{order.order_number}_{uuid.uuid4().hex[:8]}"),
            access_code=gateway_res.get("access_code"),
            checkout_url=gateway_res.get("checkout_url"),
            idempotency_key=idempotency_key,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

        saved_payment = await self.payment_repo.save_payment(payment)

        # Update order with payment reference
        order.payment_reference = saved_payment.provider_reference
        order.payment_gateway = provider.value
        await self.order_repo.create_order(order)

        return {
            "payment_id": saved_payment.id,
            "order_id": saved_payment.order_id,
            "reference": saved_payment.provider_reference,
            "provider_reference": saved_payment.provider_reference,
            "status": saved_payment.status.value,
            "amount": saved_payment.amount,
            "currency": saved_payment.currency,
            "checkout_url": saved_payment.checkout_url,
            "access_code": saved_payment.access_code,
            "is_idempotent_replay": False
        }

    async def verify_payment(self, reference: str, provider: PaymentProvider) -> Dict[str, Any]:
        payment = await self.payment_repo.get_by_provider_reference(reference)
        if not payment:
            raise PaymentNotFoundException(f"Payment with reference '{reference}' not found.")

        gateway = self.gateways.get(provider)
        if not gateway:
            raise ValueError(f"Gateway for provider {provider} not configured.")

        verification = await gateway.verify_transaction(reference)
        if verification.get("is_successful"):
            payment.status = PaymentStatus.SUCCESS
            payment.paid_at = datetime.now(timezone.utc)
            payment.gateway_response = verification.get("raw_response", {})
            payment.updated_at = datetime.now(timezone.utc)
            await self.payment_repo.save_payment(payment)

            # Mark order as PAID
            await self.order_repo.update_status(payment.order_id, OrderStatus.PAID)

            if self.notification_service:
                try:
                    order = await self.order_repo.get_by_id(payment.order_id)
                    order_dict = {
                        "customer_email": order.customer_email if order else "",
                        "customer_name": order.customer_name if order else "Valued Customer",
                        "order_number": order.order_number if order else ""
                    } if order else None
                    await self.notification_service.send_payment_receipt_email(
                        payment_data={
                            "provider_reference": payment.provider_reference,
                            "amount": payment.amount,
                            "provider": payment.provider.value if hasattr(payment.provider, "value") else str(payment.provider)
                        },
                        order_data=order_dict
                    )
                except Exception as e:
                    import logging
                    logging.getLogger("payment_service").error(f"Failed to dispatch payment receipt email: {e}")

            return {
                "verified": True,
                "status": "SUCCESS",
                "payment_id": payment.id,
                "order_id": payment.order_id,
                "amount": payment.amount
            }
        else:
            payment.status = PaymentStatus.FAILED
            payment.failure_reason = verification.get("reason", "Verification unsuccessful")
            payment.updated_at = datetime.now(timezone.utc)
            await self.payment_repo.save_payment(payment)
            return {
                "verified": False,
                "status": "FAILED",
                "payment_id": payment.id,
                "reason": payment.failure_reason
            }

    async def handle_webhook(self, provider: PaymentProvider, event_id: str, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        # Deduplication check
        if await self.payment_repo.is_webhook_processed(provider.value, event_id):
            return {"status": "ignored", "message": "Duplicate webhook event already processed"}

        reference = payload.get("data", {}).get("reference") or payload.get("reference")
        if reference:
            payment = await self.payment_repo.get_by_provider_reference(reference)
            if payment:
                payment.status = PaymentStatus.SUCCESS
                payment.paid_at = datetime.now(timezone.utc)
                payment.gateway_response = payload
                await self.payment_repo.save_payment(payment)
                await self.order_repo.update_status(payment.order_id, OrderStatus.PAID)

                if self.notification_service:
                    try:
                        order = await self.order_repo.get_by_id(payment.order_id)
                        order_dict = {
                            "customer_email": order.customer_email if order else "",
                            "customer_name": order.customer_name if order else "Valued Customer",
                            "order_number": order.order_number if order else ""
                        } if order else None
                        await self.notification_service.send_payment_receipt_email(
                            payment_data={
                                "provider_reference": payment.provider_reference,
                                "amount": payment.amount,
                                "provider": payment.provider.value if hasattr(payment.provider, "value") else str(payment.provider)
                            },
                            order_data=order_dict
                        )
                    except Exception as e:
                        import logging
                        logging.getLogger("payment_service").error(f"Failed to dispatch payment receipt email: {e}")

        event = ProcessedWebhookEvent(
            id=str(uuid.uuid4()),
            provider=provider.value,
            event_id=event_id,
            event_type=event_type,
            processed_at=datetime.now(timezone.utc),
            raw_payload=payload
        )
        await self.payment_repo.record_webhook_event(event)
        return {"status": "success", "message": f"Webhook {event_type} handled successfully"}

    def get_supported_gateways(self) -> Dict[str, Any]:
        return {
            "gateways": [
                {
                    "provider": "PAYSTACK",
                    "name": "Paystack",
                    "methods": ["card", "bank_transfer", "ussd", "qr"],
                    "currencies": ["NGN", "USD"],
                    "is_active": True
                },
                {
                    "provider": "FLUTTERWAVE",
                    "name": "Flutterwave",
                    "methods": ["card", "bank_transfer", "ussd", "barter", "mobilemoney"],
                    "currencies": ["NGN", "USD", "EUR", "GBP"],
                    "is_active": True
                },
                {
                    "provider": "OPAY",
                    "name": "OPay",
                    "methods": ["wallet", "card", "bank_transfer", "qr"],
                    "currencies": ["NGN"],
                    "is_active": True
                },
                {
                    "provider": "BANK_TRANSFER",
                    "name": "Direct Company Bank Transfer",
                    "account_name": self.bank_details.get("account_name"),
                    "bank_name": self.bank_details.get("bank_name"),
                    "account_number": self.bank_details.get("account_number"),
                    "whatsapp_confirmation": self.bank_details.get("whatsapp_number"),
                    "currencies": ["NGN"],
                    "is_active": True
                }
            ]
        }
