from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any

class PaymentStatus(str, Enum):
    INITIATED = "INITIATED"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"

class PaymentProvider(str, Enum):
    PAYSTACK = "PAYSTACK"
    FLUTTERWAVE = "FLUTTERWAVE"
    OPAY = "OPAY"
    BANK_TRANSFER = "BANK_TRANSFER"

@dataclass
class Payment:
    id: str
    order_id: str
    amount: float
    provider: PaymentProvider
    provider_reference: str
    idempotency_key: str
    user_id: Optional[str] = None
    currency: str = "NGN"
    status: PaymentStatus = PaymentStatus.INITIATED
    access_code: Optional[str] = None
    checkout_url: Optional[str] = None
    channel: Optional[str] = None
    gateway_response: Dict[str, Any] = field(default_factory=dict)
    failure_reason: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    paid_at: Optional[datetime] = None

@dataclass
class ProcessedWebhookEvent:
    id: str
    provider: str
    event_id: str
    event_type: str
    payload_hash: Optional[str] = None
    processed_at: Optional[datetime] = None
    raw_payload: Dict[str, Any] = field(default_factory=dict)
