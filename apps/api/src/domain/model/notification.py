from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional, Dict, Any

class NotificationType(str, Enum):
    EMAIL_VERIFICATION_OTP = "EMAIL_VERIFICATION_OTP"
    ORDER_CONFIRMATION = "ORDER_CONFIRMATION"
    PAYMENT_RECEIPT = "PAYMENT_RECEIPT"
    ORDER_STATUS_UPDATE = "ORDER_STATUS_UPDATE"

@dataclass
class NotificationMessage:
    recipient_email: str
    recipient_name: str
    notification_type: NotificationType
    subject: str
    html_content: str
    text_content: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    sent_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
