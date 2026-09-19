from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class NotificationUseCase(ABC):
    @abstractmethod
    async def send_verification_otp_email(self, email: str, name: str, otp: str) -> bool:
        """Sends a 6-digit OTP email verification message."""
        pass

    @abstractmethod
    async def send_order_confirmation_email(self, order_data: Dict[str, Any]) -> bool:
        """Sends order placement confirmation with itemized details."""
        pass

    @abstractmethod
    async def send_payment_receipt_email(self, payment_data: Dict[str, Any], order_data: Optional[Dict[str, Any]] = None) -> bool:
        """Sends a formal payment receipt with reference and amount."""
        pass

    @abstractmethod
    async def send_order_tracking_email(self, order_data: Dict[str, Any], tracking_status: str, tracking_note: Optional[str] = None) -> bool:
        """Sends order tracking status change notification."""
        pass
