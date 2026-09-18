from src.domain.exception.base import DomainException

from apps.api.src.application.Enum import Error_Message


class UserAlreadyExistsException(DomainException):
    def __init__(self, message: str = Error_Message.USER_ALREADY_EXISTS.value, data: dict = None):
        if data is None:
            data = {"userExist": True, "userSetUpPassword": True}
        super().__init__(message=message, status_code=200, data=data)

class UserNotFoundException(DomainException):
    def __init__(self, message: str = Error_Message.USER_NOT_FOUND.value):
        super().__init__(message=message, status_code=404)

class InvalidCredentialsException(DomainException):
    def __init__(self, message: str = Error_Message.INVALID_CREDENTIALS.value):
        super().__init__(message=message, status_code=401)

class UnauthorizedException(DomainException):
    def __init__(self, message: str = "Authentication required"):
        super().__init__(message=message, status_code=401)

class ForbiddenException(DomainException):
    def __init__(self, message: str = Error_Message.ACCESS_DENIED.value):
        super().__init__(message=message, status_code=403)

class ProductNotFoundException(DomainException):
    def __init__(self, message: str = Error_Message.PRODUCT_NOT_FOUND.value):
        super().__init__(message=message, status_code=404)

class CategoryNotFoundException(DomainException):
    def __init__(self, message: str = Error_Message.CATEGORY_NOT_FOUND.value):
        super().__init__(message=message, status_code=404)

class OrderNotFoundException(DomainException):
    def __init__(self, message: str = Error_Message.ORDER_NOT_FOUND.value):
        super().__init__(message=message, status_code=404)

class InvalidOrderStateException(DomainException):
    def __init__(self, message: str = Error_Message.INVALID_ORDER_STATE_TRANSITION.value):
        super().__init__(message=message, status_code=400)

class PaymentNotFoundException(DomainException):
    def __init__(self, message: str = Error_Message.PAYMENT_NOT_FOUND.value):
        super().__init__(message=message, status_code=404)

class PaymentFailedException(DomainException):
    def __init__(self, message: str = Error_Message. PAYMENT_PROCESSING_FAILED.value, data: dict = None):
        super().__init__(message=message, status_code=400, data=data)

class DuplicateTransactionException(DomainException):
    def __init__(self, message: str = Error_Message.TRANSACTION_ALREADY_PROCESSED.value):
        super().__init__(message=message, status_code=409)

class InvalidWebhookSignatureException(DomainException):
    def __init__(self, message: str = Error_Message.INVALID_WEBHOOK_SIGNATURE.value):
        super().__init__(message=message, status_code=401)

class CartNotFoundException(DomainException):
    def __init__(self, message: str = Error_Message.CART_NOT_FOUND.value):
        super().__init__(message=message, status_code=404)

class CartItemNotFoundException(DomainException):
    def __init__(self, message: str = Error_Message.CART_ITEM_NOT_FOUND.value):
        super().__init__(message=message, status_code=404)

class ConfigurationNotFoundException(DomainException):
    def __init__(self, message: str = Error_Message.CONFIGURATION_NOT_FOUND.value):
        super().__init__(message=message, status_code=404)
