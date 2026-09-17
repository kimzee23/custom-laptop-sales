from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any

class PaymentStatus(str, Enum):
    INITIATED = "INITIATED"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"

class PaymentProviderType(str, Enum):
    PAYSTACK = "PAYSTACK"
    FLUTTERWAVE = "FLUTTERWAVE"
    OPAY = "OPAY"
    BANK_TRANSFER = "BANK_TRANSFER"

@dataclass(frozen=True)
class PaymentRequest:
    order_id: str
    order_number: str
    amount: float
    currency: str
    customer_email: str
    customer_name: str
    customer_phone: Optional[str] = None
    callback_url: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    idempotency_key: str = ""

@dataclass(frozen=True)
class PaymentInitializationResult:
    provider: PaymentProviderType
    provider_reference: str
    checkout_url: str
    access_code: Optional[str] = None
    raw_response: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class PaymentVerificationResult:
    provider: PaymentProviderType
    provider_reference: str
    status: PaymentStatus
    amount: float
    currency: str
    channel: Optional[str] = None
    paid_at: Optional[datetime] = None
    gateway_message: Optional[str] = None
    raw_response: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class ParsedWebhookEvent:
    provider: PaymentProviderType
    event_id: str
    event_type: str
    provider_reference: str
    status: PaymentStatus
    amount: float
    currency: str
    paid_at: Optional[datetime] = None
    raw_payload: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class PaymentCompletedEvent:
    payment_id: str
    order_id: str
    order_number: str
    provider: PaymentProviderType
    provider_reference: str
    amount: float
    currency: str
    customer_email: str
    customer_name: str
    completed_at: datetime
