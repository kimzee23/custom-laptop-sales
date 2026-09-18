import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from src.domain.model.user import User
from src.domain.exception.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
    InvalidCredentialsException,
    ForbiddenException
)
from src.application.ports.inbound.auth_usecase import AuthUseCase
from src.application.ports.outbound.user_repository_port import UserRepositoryPort

class AuthService(AuthUseCase):
    def __init__(self, user_repository: UserRepositoryPort, hash_pw_fn, verify_pw_fn, create_token_fn):
        self.user_repo = user_repository
        self.hash_password = hash_pw_fn
        self.verify_password = verify_pw_fn
        self.create_access_token = create_token_fn

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
        new_user = User(
            id=str(uuid.uuid4()),
            name=name.strip(),
            email=normalized_email,
            hashed_password=hashed,
            phone=phone,
            role="customer",
            reward_points=500,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        saved_user = await self.user_repo.save(new_user)
        token = self.create_access_token({"sub": saved_user.id, "email": saved_user.email, "role": saved_user.role})
        return {
            "access_token": token,
            "token": token,
            "token_type": "bearer",
            "user": {
                "id": saved_user.id,
                "name": saved_user.name,
                "email": saved_user.email,
                "role": saved_user.role,
                "reward_points": saved_user.reward_points
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
