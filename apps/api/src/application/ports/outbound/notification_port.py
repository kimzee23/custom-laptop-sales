from abc import ABC, abstractmethod
from src.domain.model.notification import NotificationMessage

class NotificationPort(ABC):
    @abstractmethod
    async def send_email(self, message: NotificationMessage) -> bool:
        """Sends an email notification. Returns True if successfully dispatched or queued."""
        pass
