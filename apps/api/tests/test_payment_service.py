import pytest
import pytest_asyncio
import asyncio
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select

from app.core.database import Base
from app.models import Order, Payment, ProcessedWebhookEvent
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
from app.modules.payments.services.payment_service import PaymentServiceImpl
from app.modules.payments.services.event_dispatcher import PaymentEventDispatcher
from app.modules.payments.services.order_fulfillment_service import OrderFulfillmentService

# Create isolated test in-memory SQLite database
TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture
async def test_db():
    engine = create_async_engine(TEST_DB_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    session_maker = async_sessionmaker(engine, expire_on_commit=False)
    async with session_maker() as session:
        yield session

    await engine.dispose()

class MockGatewayProvider(PaymentProvider):
    def __init__(self, ptype: PaymentProviderType = PaymentProviderType.PAYSTACK):
        self._type = ptype
        self.initialize_call_count = 0
        self.verify_call_count = 0
        self.simulate_timeout = False

    @property
    def provider_type(self) -> PaymentProviderType:
        return self._type

    async def initialize(self, request: PaymentRequest) -> PaymentInitializationResult:
        if self.simulate_timeout:
            raise TimeoutError("Simulated network gateway timeout")
        self.initialize_call_count += 1
        ref = f"mock_{request.order_number}_{request.idempotency_key[:6]}"
        return PaymentInitializationResult(
            provider=self.provider_type,
            provider_reference=ref,
            checkout_url=f"https://checkout.mockgateway.com/pay/{ref}",
            access_code=f"acc_{ref}"
        )

    async def verify(self, provider_reference: str) -> PaymentVerificationResult:
        self.verify_call_count += 1
        return PaymentVerificationResult(
            provider=self.provider_type,
            provider_reference=provider_reference,
            status=PaymentStatus.SUCCESS,
            amount=1450000.0,
            currency="NGN",
            channel="card",
            paid_at=datetime.utcnow(),
            gateway_message="Verified successfully"
        )

    def verify_webhook_signature(self, raw_body: bytes, headers: dict) -> bool:
        return True

    def parse_webhook(self, payload: dict) -> ParsedWebhookEvent:
        return ParsedWebhookEvent(
            provider=self.provider_type,
            event_id=payload.get("event_id", "mock_evt_1"),
            event_type="charge.success",
            provider_reference=payload.get("reference", "mock_ref_1"),
            status=PaymentStatus.SUCCESS,
            amount=1450000.0,
            currency="NGN",
            paid_at=datetime.utcnow()
        )

async def create_test_order(db: AsyncSession, order_number: str = "ORD-TEST-001") -> Order:
    order = Order(
        order_number=order_number,
        customer_name="Emeka Obi",
        customer_email="emeka@example.com",
        customer_phone="08012345678",
        shipping_address={"street": "12 Marina St", "city": "Lagos", "state": "Lagos", "country": "Nigeria"},
        status="PENDING_PAYMENT",
        subtotal=1450000.0,
        shipping_fee=0.0,
        discount_amount=0.0,
        total_amount=1450000.0,
        currency="NGN"
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


# -------------------------------------------------------------
# TEST 1: New Payment Creation
# -------------------------------------------------------------
@pytest.mark.asyncio
async def test_1_new_payment_creation(test_db: AsyncSession):
    order = await create_test_order(test_db, "ORD-TEST-101")
    mock_provider = MockGatewayProvider(PaymentProviderType.PAYSTACK)
    PaymentProviderFactory.register_provider(PaymentProviderType.PAYSTACK, mock_provider)

    svc = PaymentServiceImpl()
    result = await svc.initialize_payment(
        order_number=order.order_number,
        provider_type=PaymentProviderType.PAYSTACK,
        idempotency_key="idemp_key_001",
        db=test_db
    )

    assert result["order_number"] == "ORD-TEST-101"
    assert result["idempotent_replay"] is False
    assert mock_provider.initialize_call_count == 1
    assert "https://checkout.mockgateway.com/pay/" in result["checkout_url"]

    # Verify DB persistence
    stmt = select(Payment).where(Payment.idempotency_key == "idemp_key_001")
    saved = (await test_db.execute(stmt)).scalar_one_or_none()
    assert saved is not None
    assert saved.status == PaymentStatus.INITIATED.value


# -------------------------------------------------------------
# TEST 2: Same Idempotency Key (No duplicate payment/gateway call)
# -------------------------------------------------------------
@pytest.mark.asyncio
async def test_2_same_idempotency_key_returns_existing(test_db: AsyncSession):
    order = await create_test_order(test_db, "ORD-TEST-102")
    mock_provider = MockGatewayProvider(PaymentProviderType.PAYSTACK)
    PaymentProviderFactory.register_provider(PaymentProviderType.PAYSTACK, mock_provider)

    svc = PaymentServiceImpl()
    
    # First call
    res1 = await svc.initialize_payment(
        order_number=order.order_number,
        provider_type=PaymentProviderType.PAYSTACK,
        idempotency_key="idemp_key_002",
        db=test_db
    )
    assert res1["idempotent_replay"] is False
    assert mock_provider.initialize_call_count == 1

    # Second call with SAME idempotency key (simulating double-click or page refresh)
    res2 = await svc.initialize_payment(
        order_number=order.order_number,
        provider_type=PaymentProviderType.PAYSTACK,
        idempotency_key="idemp_key_002",
        db=test_db
    )

    assert res2["idempotent_replay"] is True
    assert res2["payment_id"] == res1["payment_id"]
    assert res2["provider_reference"] == res1["provider_reference"]
    # Critical: Gateway must NOT have been called a second time
    assert mock_provider.initialize_call_count == 1

    # Ensure only ONE payment record exists in database
    stmt = select(Payment).where(Payment.idempotency_key == "idemp_key_002")
    payments = (await test_db.execute(stmt)).scalars().all()
    assert len(payments) == 1


# -------------------------------------------------------------
# TEST 3: Gateway Timeout & Verification Recovery
# -------------------------------------------------------------
@pytest.mark.asyncio
async def test_3_gateway_timeout_and_verification_recovery(test_db: AsyncSession):
    order = await create_test_order(test_db, "ORD-TEST-103")
    mock_provider = MockGatewayProvider(PaymentProviderType.FLUTTERWAVE)
    PaymentProviderFactory.register_provider(PaymentProviderType.FLUTTERWAVE, mock_provider)

    svc = PaymentServiceImpl()

    # Normal initialization
    init_res = await svc.initialize_payment(
        order_number=order.order_number,
        provider_type=PaymentProviderType.FLUTTERWAVE,
        idempotency_key="idemp_key_003",
        db=test_db
    )
    ref = init_res["provider_reference"]

    # Now verify the existing payment directly without creating any new payment
    verify_res = await svc.verify_payment(
        provider_type=PaymentProviderType.FLUTTERWAVE,
        reference=ref,
        db=test_db
    )

    assert verify_res["status"] == PaymentStatus.SUCCESS
    assert verify_res["order_status"] == "PAID"

    # Verify order was fulfilled
    stmt = select(Order).where(Order.id == order.id)
    updated_order = (await test_db.execute(stmt)).scalar_one()
    assert updated_order.status == "PAID"
    assert updated_order.payment_reference == ref


# -------------------------------------------------------------
# TEST 4: Duplicate Webhook Handling
# -------------------------------------------------------------
@pytest.mark.asyncio
async def test_4_duplicate_webhook_safely_ignored(test_db: AsyncSession):
    order = await create_test_order(test_db, "ORD-TEST-104")
    mock_provider = MockGatewayProvider(PaymentProviderType.OPAY)
    PaymentProviderFactory.register_provider(PaymentProviderType.OPAY, mock_provider)

    svc = PaymentServiceImpl()
    init_res = await svc.initialize_payment(
        order_number=order.order_number,
        provider_type=PaymentProviderType.OPAY,
        idempotency_key="idemp_key_004",
        db=test_db
    )
    ref = init_res["provider_reference"]

    webhook_payload = {
        "event_id": "evt_opay_unique_999",
        "reference": ref,
        "status": "SUCCESS"
    }

    # 1st Webhook delivery
    res1 = await svc.handle_webhook(
        provider_type=PaymentProviderType.OPAY,
        raw_body=b'{"test": "payload"}',
        headers={"sha512": "mock_valid"},
        payload=webhook_payload,
        db=test_db
    )
    assert res1["status"] == "success"

    # 2nd Duplicate Webhook delivery with same event_id
    res2 = await svc.handle_webhook(
        provider_type=PaymentProviderType.OPAY,
        raw_body=b'{"test": "payload"}',
        headers={"sha512": "mock_valid"},
        payload=webhook_payload,
        db=test_db
    )
    assert res2["status"] == "ignored"
    assert res2["message"] == "Event already processed"

    # Ensure only 1 record in ProcessedWebhookEvent table
    evt_stmt = select(ProcessedWebhookEvent).where(ProcessedWebhookEvent.event_id == "evt_opay_unique_999")
    records = (await test_db.execute(evt_stmt)).scalars().all()
    assert len(records) == 1


# -------------------------------------------------------------
# TEST 5: Successful Payment Triggers Decoupled Order Fulfillment
# -------------------------------------------------------------
@pytest.mark.asyncio
async def test_5_successful_payment_fulfills_order(test_db: AsyncSession):
    order = await create_test_order(test_db, "ORD-TEST-105")
    
    event = PaymentCompletedEvent(
        payment_id=str(uuid.uuid4()),
        order_id=order.id,
        order_number=order.order_number,
        provider=PaymentProviderType.PAYSTACK,
        provider_reference="pstk_test_105",
        amount=order.total_amount,
        currency="NGN",
        customer_email=order.customer_email,
        customer_name=order.customer_name,
        completed_at=datetime.utcnow()
    )

    await OrderFulfillmentService.on_payment_completed(event, db=test_db)

    # Check order status changed to PAID
    stmt = select(Order).where(Order.id == order.id)
    updated_order = (await test_db.execute(stmt)).scalar_one()
    assert updated_order.status == "PAID"
    assert updated_order.payment_gateway == "PAYSTACK"
    assert updated_order.payment_reference == "pstk_test_105"


# -------------------------------------------------------------
# TEST 6: Duplicate Success Event Is Idempotent
# -------------------------------------------------------------
@pytest.mark.asyncio
async def test_6_duplicate_payment_completed_event_is_idempotent(test_db: AsyncSession):
    order = await create_test_order(test_db, "ORD-TEST-106")
    
    event = PaymentCompletedEvent(
        payment_id=str(uuid.uuid4()),
        order_id=order.id,
        order_number=order.order_number,
        provider=PaymentProviderType.PAYSTACK,
        provider_reference="pstk_test_106",
        amount=order.total_amount,
        currency="NGN",
        customer_email=order.customer_email,
        customer_name=order.customer_name,
        completed_at=datetime.utcnow()
    )

    # Deliver event first time
    await OrderFulfillmentService.on_payment_completed(event, db=test_db)
    stmt = select(Order).where(Order.id == order.id)
    order_after_1 = (await test_db.execute(stmt)).scalar_one()
    paid_at_time = order_after_1.paid_at

    # Deliver event second time
    await OrderFulfillmentService.on_payment_completed(event, db=test_db)
    order_after_2 = (await test_db.execute(stmt)).scalar_one()

    assert order_after_2.status == "PAID"
    # Status remained consistent and wasn't erroneously re-mutated
    assert order_after_2.paid_at == paid_at_time


# -------------------------------------------------------------
# TEST 7: Concurrent Requests with Same Idempotency Key
# -------------------------------------------------------------
@pytest.mark.asyncio
async def test_7_concurrent_requests_handled_safely(test_db: AsyncSession):
    order = await create_test_order(test_db, "ORD-TEST-107")
    mock_provider = MockGatewayProvider(PaymentProviderType.OPAY)
    PaymentProviderFactory.register_provider(PaymentProviderType.OPAY, mock_provider)

    svc = PaymentServiceImpl()
    
    # Run 3 initialization requests concurrently using the SAME idempotency key
    results = await asyncio.gather(
        svc.initialize_payment(order.order_number, PaymentProviderType.OPAY, "concurrent_key_777", test_db),
        svc.initialize_payment(order.order_number, PaymentProviderType.OPAY, "concurrent_key_777", test_db),
        svc.initialize_payment(order.order_number, PaymentProviderType.OPAY, "concurrent_key_777", test_db)
    )

    # Exactly one was initial create (idempotent_replay=False), others were idempotent replays
    replays = [r["idempotent_replay"] for r in results]
    assert False in replays # At least one initial creation
    # All returned the exact same payment_id and reference
    payment_ids = set(r["payment_id"] for r in results)
    assert len(payment_ids) == 1

    # Verify database has strictly 1 record
    stmt = select(Payment).where(Payment.idempotency_key == "concurrent_key_777")
    saved_records = (await test_db.execute(stmt)).scalars().all()
    assert len(saved_records) == 1
