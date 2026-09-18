import os
from typing import List, Union
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Custom Laptop Store API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "super-secret-key-change-in-production-min-32-chars"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # CORS
    BACKEND_CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]

    @property
    def cors_origins(self) -> List[str]:
        if isinstance(self.BACKEND_CORS_ORIGINS, list):
            return self.BACKEND_CORS_ORIGINS
        if isinstance(self.BACKEND_CORS_ORIGINS, str):
            if self.BACKEND_CORS_ORIGINS.strip() == "*":
                return ["*"]
            return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",") if origin.strip()]
        return ["*"]

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite+aiosqlite:///./laptop_store.db"
    )
    SYNC_DATABASE_URL: str = os.getenv(
        "SYNC_DATABASE_URL",
        "sqlite:///./laptop_store.db"
    )

    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Currency
    CURRENCY: str = "NGN"
    CURRENCY_SYMBOL: str = "₦"

    # Frontend URL
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

    # Paystack Settings
    PAYSTACK_SECRET_KEY: str = os.getenv("PAYSTACK_SECRET_KEY", "sk_test_mock_paystack_secret_key_12345")
    PAYSTACK_PUBLIC_KEY: str = os.getenv("PAYSTACK_PUBLIC_KEY", "pk_test_mock_paystack_public_key_12345")
    PAYSTACK_BASE_URL: str = os.getenv("PAYSTACK_BASE_URL", "https://api.paystack.co")

    # Flutterwave Settings
    FLUTTERWAVE_SECRET_KEY: str = os.getenv("FLUTTERWAVE_SECRET_KEY", "FLWSECK_TEST-mock_secret_key_12345-X")
    FLUTTERWAVE_PUBLIC_KEY: str = os.getenv("FLUTTERWAVE_PUBLIC_KEY", "FLWPUBK_TEST-mock_public_key_12345-X")
    FLUTTERWAVE_SECRET_HASH: str = os.getenv("FLUTTERWAVE_SECRET_HASH", "mock_flw_secret_hash_custom_laptop_store")
    FLUTTERWAVE_BASE_URL: str = os.getenv("FLUTTERWAVE_BASE_URL", "https://api.flutterwave.com/v3")

    # OPay Settings
    OPAY_MERCHANT_ID: str = os.getenv("OPAY_MERCHANT_ID", "256621000000001")
    OPAY_SECRET_KEY: str = os.getenv("OPAY_SECRET_KEY", "mock_opay_secret_key_abcdef123456")
    OPAY_PUBLIC_KEY: str = os.getenv("OPAY_PUBLIC_KEY", "mock_opay_public_key_abcdef123456")
    OPAY_BASE_URL: str = os.getenv("OPAY_BASE_URL", "https://cashierapi.opayweb.com")
    OPAY_ENV: str = os.getenv("OPAY_ENV", "test")

    # Company Bank Account Settings
    COMPANY_BANK_NAME: str = os.getenv("COMPANY_BANK_NAME", "Guaranty Trust Bank (GTBank)")
    COMPANY_ACCOUNT_NAME: str = os.getenv("COMPANY_ACCOUNT_NAME", "Custom Laptop Sales Nigeria Ltd")
    COMPANY_ACCOUNT_NUMBER: str = os.getenv("COMPANY_ACCOUNT_NUMBER", "0123456789")
    COMPANY_WHATSAPP_NUMBER: str = os.getenv("COMPANY_WHATSAPP_NUMBER", "+2347084256460")

    model_config = {
        "case_sensitive": True,
        "env_file": ".env",
        "extra": "allow"
    }

settings = Settings()
