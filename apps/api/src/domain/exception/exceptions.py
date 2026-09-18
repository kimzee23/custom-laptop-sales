from src.domain.exception.base import DomainException

class UserAlreadyExistsException(DomainException):
    def __init__(self, message: str = "User exist", data: dict = None):
        if data is None:
            data = {"userExist": True, "userSetUpPassword": True}
        super().__init__(message=message, status_code=200, data=data)

class UserNotFoundException(DomainException):
    def __init__(self, message: str = "User not found"):
        super().__init__(message=message, status_code=404)

class InvalidCredentialsException(DomainException):
    def __init__(self, message: str = "Invalid email or password"):
        super().__init__(message=message, status_code=401)

class UnauthorizedException(DomainException):
    def __init__(self, message: str = "Authentication required"):
        super().__init__(message=message, status_code=401)

class ForbiddenException(DomainException):
    def __init__(self, message: str = "Permission denied"):
        super().__init__(message=message, status_code=403)

class ProductNotFoundException(DomainException):
    def __init__(self, message: str = "Product not found"):
        super().__init__(message=message, status_code=404)

class CategoryNotFoundException(DomainException):
    def __init__(self, message: str = "Category not found"):
        super().__init__(message=message, status_code=404)

class OrderNotFoundException(DomainException):
    def __init__(self, message: str = "Order not found"):
        super().__init__(message=message, status_code=404)

class InvalidOrderStateException(DomainException):
    def __init__(self, message: str = "Invalid order state transition"):
        super().__init__(message=message, status_code=400)

class PaymentNotFoundException(DomainException):
    def __init__(self, message: str = "Payment not found"):
        super().__init__(message=message, status_code=404)

class PaymentFailedException(DomainException):
    def __init__(self, message: str = "Payment processing failed", data: dict = None):
        super().__init__(message=message, status_code=400, data=data)

class DuplicateTransactionException(DomainException):
    def __init__(self, message: str = "Transaction already processed"):
        super().__init__(message=message, status_code=409)

class InvalidWebhookSignatureException(DomainException):
    def __init__(self, message: str = "Invalid webhook signature"):
        super().__init__(message=message, status_code=401)

class CartNotFoundException(DomainException):
    def __init__(self, message: str = "Cart not found"):
        super().__init__(message=message, status_code=404)

class CartItemNotFoundException(DomainException):
    def __init__(self, message: str = "Cart item not found"):
        super().__init__(message=message, status_code=404)

class ConfigurationNotFoundException(DomainException):
    def __init__(self, message: str = "Configuration option not found"):
        super().__init__(message=message, status_code=404)
