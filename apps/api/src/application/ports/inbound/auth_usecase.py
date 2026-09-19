from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from src.domain.model.user import User

class AuthUseCase(ABC):
    @abstractmethod
    async def register(self, name: str, email: str, password: str, phone: Optional[str] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def login(self, email: str, password: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def check_user(self, email: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_current_user_profile(self, user_id: str) -> User:
        pass

    @abstractmethod
    async def update_profile(self, user_id: str, name: Optional[str] = None, phone: Optional[str] = None, avatar_url: Optional[str] = None) -> User:
        pass

    @abstractmethod
    async def change_password(self, user_id: str, current_password: str, new_password: str) -> bool:
        pass

    @abstractmethod
    async def admin_login(self, email: str, password: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def verify_email_otp(self, email: str, otp: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def resend_email_otp(self, email: str) -> Dict[str, Any]:
        pass

