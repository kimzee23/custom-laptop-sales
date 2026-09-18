from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from src.infrastructure.adapters.outbound.persistence.database import get_db_session
from src.infrastructure.config.security import (
    security, hash_password, verify_password, create_access_token, decode_access_token
)
from src.infrastructure.config.settings import settings
from src.domain.model.payment import PaymentProvider

# Repositories
from src.infrastructure.adapters.outbound.persistence.repositories.user_repository import UserRepository
from src.infrastructure.adapters.outbound.persistence.repositories.product_repository import ProductRepository
from src.infrastructure.adapters.outbound.persistence.repositories.configuration_repository import ConfigurationRepository
from src.infrastructure.adapters.outbound.persistence.repositories.cart_repository import CartRepository
from src.infrastructure.adapters.outbound.persistence.repositories.order_repository import OrderRepository
from src.infrastructure.adapters.outbound.persistence.repositories.payment_repository import PaymentRepository
from src.infrastructure.adapters.outbound.persistence.repositories.analytics_repository import AnalyticsRepository
from src.infrastructure.adapters.outbound.persistence.repositories.review_repository import ReviewRepository

# Gateway Adapters
from src.infrastructure.adapters.outbound.external.paystack_adapter import PaystackAdapter
from src.infrastructure.adapters.outbound.external.flutterwave_adapter import FlutterwaveAdapter
from src.infrastructure.adapters.outbound.external.opay_adapter import OPayAdapter
from src.infrastructure.adapters.outbound.external.bank_transfer_adapter import BankTransferAdapter
from src.infrastructure.adapters.outbound.external.local_storage_adapter import LocalStorageAdapter

# Services
from src.application.service.auth_service import AuthService
from src.application.service.product_service import ProductService
from src.application.service.configuration_service import ConfigurationService
from src.application.service.cart_service import CartService
from src.application.service.order_service import OrderService
from src.application.service.payment_service import PaymentService
from src.application.service.analytics_service import AnalyticsService
from src.application.service.artwork_service import ArtworkService
from src.application.service.review_service import ReviewService
from src.application.service.admin_service import AdminService
from src.application.service.health_service import HealthService

# Dependency Providers
def get_user_repository(session: AsyncSession = Depends(get_db_session)) -> UserRepository:
    return UserRepository(session)

def get_product_repository(session: AsyncSession = Depends(get_db_session)) -> ProductRepository:
    return ProductRepository(session)

def get_configuration_repository(session: AsyncSession = Depends(get_db_session)) -> ConfigurationRepository:
    return ConfigurationRepository(session)

def get_cart_repository(session: AsyncSession = Depends(get_db_session)) -> CartRepository:
    return CartRepository(session)

def get_order_repository(session: AsyncSession = Depends(get_db_session)) -> OrderRepository:
    return OrderRepository(session)

def get_payment_repository(session: AsyncSession = Depends(get_db_session)) -> PaymentRepository:
    return PaymentRepository(session)

def get_analytics_repository(session: AsyncSession = Depends(get_db_session)) -> AnalyticsRepository:
    return AnalyticsRepository(session)

def get_review_repository(session: AsyncSession = Depends(get_db_session)) -> ReviewRepository:
    return ReviewRepository(session)

# Service Providers
def get_auth_service(user_repo: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(
        user_repository=user_repo,
        hash_pw_fn=hash_password,
        verify_pw_fn=verify_password,
        create_token_fn=create_access_token
    )

def get_product_service(product_repo: ProductRepository = Depends(get_product_repository)) -> ProductService:
    return ProductService(product_repository=product_repo)

def get_configuration_service(
    config_repo: ConfigurationRepository = Depends(get_configuration_repository),
    product_repo: ProductRepository = Depends(get_product_repository)
) -> ConfigurationService:
    return ConfigurationService(config_repository=config_repo, product_repository=product_repo)

def get_cart_service(cart_repo: CartRepository = Depends(get_cart_repository)) -> CartService:
    return CartService(cart_repository=cart_repo)

def get_order_service(order_repo: OrderRepository = Depends(get_order_repository)) -> OrderService:
    return OrderService(order_repository=order_repo)

def get_payment_service(
    payment_repo: PaymentRepository = Depends(get_payment_repository),
    order_repo: OrderRepository = Depends(get_order_repository)
) -> PaymentService:
    gateways = {
        PaymentProvider.PAYSTACK: PaystackAdapter(),
        PaymentProvider.FLUTTERWAVE: FlutterwaveAdapter(),
        PaymentProvider.OPAY: OPayAdapter(),
        PaymentProvider.BANK_TRANSFER: BankTransferAdapter()
    }
    company_bank = {
        "bank_name": settings.COMPANY_BANK_NAME,
        "account_name": settings.COMPANY_ACCOUNT_NAME,
        "account_number": settings.COMPANY_ACCOUNT_NUMBER,
        "whatsapp_number": settings.COMPANY_WHATSAPP_NUMBER
    }
    return PaymentService(
        payment_repository=payment_repo,
        order_repository=order_repo,
        gateway_adapters=gateways,
        company_bank_details=company_bank
    )

def get_analytics_service(analytics_repo: AnalyticsRepository = Depends(get_analytics_repository)) -> AnalyticsService:
    return AnalyticsService(analytics_repository=analytics_repo)

def get_artwork_service() -> ArtworkService:
    return ArtworkService(storage_port=LocalStorageAdapter())

def get_review_service(review_repo: ReviewRepository = Depends(get_review_repository)) -> ReviewService:
    return ReviewService(review_repository=review_repo)

def get_admin_service(
    order_repo: OrderRepository = Depends(get_order_repository),
    product_repo: ProductRepository = Depends(get_product_repository),
    user_repo: UserRepository = Depends(get_user_repository)
) -> AdminService:
    return AdminService(order_repo=order_repo, product_repo=product_repo, user_repo=user_repo)

async def check_db_health() -> bool:
    try:
        from sqlalchemy import text
        from src.infrastructure.adapters.outbound.persistence.database import async_engine
        async with async_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False

def get_health_service() -> HealthService:
    return HealthService(db_check_fn=check_db_health)

# Security Current User Dependencies
async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
):
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please provide a valid Bearer token.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    payload = decode_access_token(credentials.credentials)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return await auth_service.get_current_user_profile(payload["sub"])

async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
):
    if not credentials or not credentials.credentials:
        return None
    payload = decode_access_token(credentials.credentials)
    if not payload or "sub" not in payload:
        return None
    try:
        return await auth_service.get_current_user_profile(payload["sub"])
    except Exception:
        return None

async def get_current_admin(
    current_user = Depends(get_optional_user)
):
    if current_user and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrative privileges required to access this endpoint."
        )
    return current_user
