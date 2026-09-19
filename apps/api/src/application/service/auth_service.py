import uuid
import secrets
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional
from src.domain.model.user import User
from src.domain.exception.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
    InvalidCredentialsException,
    ForbiddenException,
    InvalidOtpException,
    OtpExpiredException
)
from src.application.ports.inbound.auth_usecase import AuthUseCase
from src.application.ports.inbound.notification_usecase import NotificationUseCase
from src.application.ports.outbound.user_repository_port import UserRepositoryPort

class AuthService(AuthUseCase):
    def __init__(self, user_repository: UserRepositoryPort, hash_pw_fn, verify_pw_fn, create_token_fn, notification_service: Optional[NotificationUseCase] = None):
        self.user_repo = user_repository
        self.hash_password = hash_pw_fn
        self.verify_password = verify_pw_fn
        self.create_access_token = create_token_fn
        self.notification_service = notification_service

    async def check_user(self, email: str) -> Dict[str, Any]:
        normalized_email = email.lower().strip()
        user = await self.user_repo.get_by_email(normalized_email)
        if user:
            return {
                "userExist": True,
                "userSetUpPassword": bool(user.hashed_password)
            }
        return {
            "userExist": False,
            "userSetUpPassword": False
        }

    async def register(self, name: str, email: str, password: str, phone: Optional[str] = None) -> Dict[str, Any]:
        normalized_email = email.lower().strip()
        existing = await self.user_repo.get_by_email(normalized_email)
        if existing:
            raise UserAlreadyExistsException(
                message="User exist",
                data={"userExist": True, "userSetUpPassword": bool(existing.hashed_password)}
            )

        hashed = self.hash_password(password)
        otp = f"{secrets.randbelow(900000) + 100000}"
        otp_expiry = datetime.now(timezone.utc) + timedelta(minutes=15)

        new_user = User(
            id=str(uuid.uuid4()),
            name=name.strip(),
            email=normalized_email,
            hashed_password=hashed,
            phone=phone,
            role="customer",
            reward_points=500,
            is_verified=False,
            otp_code=otp,
            otp_expires_at=otp_expiry,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        saved_user = await self.user_repo.save(new_user)

        # Dispatch OTP verification email
        if self.notification_service:
            try:
                await self.notification_service.send_verification_otp_email(saved_user.email, saved_user.name, otp)
            except Exception as e:
                import logging
                logging.getLogger("auth_service").error(f"Failed to dispatch OTP email: {e}")

        token = self.create_access_token({"sub": saved_user.id, "email": saved_user.email, "role": saved_user.role})
        return {
            "access_token": token,
            "token": token,
            "token_type": "bearer",
            "requires_verification": True,
            "is_verified": False,
            "user": {
                "id": saved_user.id,
                "name": saved_user.name,
                "email": saved_user.email,
                "role": saved_user.role,
                "reward_points": saved_user.reward_points,
                "is_verified": False
            }
        }

    async def login(self, email: str, password: str) -> Dict[str, Any]:
        normalized_email = email.lower().strip()
        user = await self.user_repo.get_by_email(normalized_email)
        if not user or not self.verify_password(password, user.hashed_password):
            raise InvalidCredentialsException("Invalid email or password.")

        token = self.create_access_token({"sub": user.id, "email": user.email, "role": user.role})
        return {
            "access_token": token,
            "token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "reward_points": user.reward_points
            }
        }

    async def get_current_user_profile(self, user_id: str) -> User:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundException()
        return user

    async def update_profile(self, user_id: str, name: Optional[str] = None, phone: Optional[str] = None, avatar_url: Optional[str] = None) -> User:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundException()
        if name is not None:
            user.name = name
        if phone is not None:
            user.phone = phone
        if avatar_url is not None:
            user.avatar_url = avatar_url
        user.updated_at = datetime.now(timezone.utc)
        return await self.user_repo.save(user)

    async def change_password(self, user_id: str, current_password: str, new_password: str) -> bool:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundException()
        if not self.verify_password(current_password, user.hashed_password):
            raise InvalidCredentialsException("Current password does not match.")
        user.hashed_password = self.hash_password(new_password)
        user.updated_at = datetime.now(timezone.utc)
        await self.user_repo.save(user)
        return True

    async def admin_login(self, email: str, password: str) -> Dict[str, Any]:
        res = await self.login(email, password)
        if res["user"]["role"] != "admin":
            raise ForbiddenException("Access denied: Administrative privileges required.")
        return res

    async def verify_email_otp(self, email: str, otp: str) -> Dict[str, Any]:
        normalized_email = email.lower().strip()
        user = await self.user_repo.get_by_email(normalized_email)
        if not user:
            raise UserNotFoundException("No account registered with this email address.")

        if user.is_verified:
            token = self.create_access_token({"sub": user.id, "email": user.email, "role": user.role})
            return {
                "verified": True,
                "access_token": token,
                "token": token,
                "token_type": "bearer",
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role,
                    "reward_points": user.reward_points,
                    "is_verified": True
                }
            }

        # Check OTP match
        if not user.otp_code or user.otp_code.strip() != otp.strip():
            raise InvalidOtpException("Invalid verification code. Please check and try again.")

        # Check expiration
        if user.otp_expires_at:
            exp = user.otp_expires_at
            if exp.tzinfo is None:
                exp = exp.replace(tzinfo=timezone.utc)
            if datetime.now(timezone.utc) > exp:
                raise OtpExpiredException("Verification code has expired. Please request a new code.")

        # Mark user verified
        user.is_verified = True
        user.otp_code = None
        user.otp_expires_at = None
        user.updated_at = datetime.now(timezone.utc)
        saved_user = await self.user_repo.save(user)

        token = self.create_access_token({"sub": saved_user.id, "email": saved_user.email, "role": saved_user.role})
        return {
            "verified": True,
            "access_token": token,
            "token": token,
            "token_type": "bearer",
            "user": {
                "id": saved_user.id,
                "name": saved_user.name,
                "email": saved_user.email,
                "role": saved_user.role,
                "reward_points": saved_user.reward_points,
                "is_verified": True
            }
        }

    async def resend_email_otp(self, email: str) -> Dict[str, Any]:
        normalized_email = email.lower().strip()
        user = await self.user_repo.get_by_email(normalized_email)
        if not user:
            raise UserNotFoundException("No account registered with this email address.")

        if user.is_verified:
            return {
                "message": "Account is already verified.",
                "already_verified": True
            }

        otp = f"{secrets.randbelow(900000) + 100000}"
        user.otp_code = otp
        user.otp_expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)
        user.updated_at = datetime.now(timezone.utc)
        await self.user_repo.save(user)

        if self.notification_service:
            try:
                await self.notification_service.send_verification_otp_email(user.email, user.name, otp)
            except Exception as e:
                import logging
                logging.getLogger("auth_service").error(f"Failed to resend OTP email: {e}")

        return {
            "sent": True,
            "message": "A new verification code has been dispatched to your email."
        }
