from typing import Dict
from app.modules.payments.domain.models import PaymentProviderType
from app.modules.payments.domain.interfaces import PaymentProvider
from app.modules.payments.providers.paystack import PaystackPaymentProvider
from app.modules.payments.providers.flutterwave import FlutterwavePaymentProvider
from app.modules.payments.providers.opay import OPayPaymentProvider
from app.modules.payments.providers.bank_transfer import BankTransferPaymentProvider

class PaymentProviderFactory:
    """
    Factory & Registry for Payment Providers.
    Decouples application layer from concrete provider instantiation.
    """
    _providers: Dict[PaymentProviderType, PaymentProvider] = {}

    @classmethod
    def get_provider(cls, provider_type: PaymentProviderType) -> PaymentProvider:
        if provider_type not in cls._providers:
            if provider_type == PaymentProviderType.PAYSTACK:
                cls._providers[provider_type] = PaystackPaymentProvider()
            elif provider_type == PaymentProviderType.FLUTTERWAVE:
                cls._providers[provider_type] = FlutterwavePaymentProvider()
            elif provider_type == PaymentProviderType.OPAY:
                cls._providers[provider_type] = OPayPaymentProvider()
            elif provider_type == PaymentProviderType.BANK_TRANSFER:
                cls._providers[provider_type] = BankTransferPaymentProvider()
            else:
                raise ValueError(f"Unsupported payment provider: {provider_type}")
        return cls._providers[provider_type]

    @classmethod
    def register_provider(cls, provider_type: PaymentProviderType, provider: PaymentProvider):
        """Allows injecting custom / mock providers for unit testing."""
        cls._providers[provider_type] = provider

    @classmethod
    def clear(cls):
        cls._providers.clear()
