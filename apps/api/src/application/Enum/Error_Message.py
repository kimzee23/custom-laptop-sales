
from enum import Enum

class Error_Message(Enum):
    USER_ALREADY_EXISTS = "User already exists"
    USER_NOT_FOUND = "User not found"
    INVALID_CREDENTIALS = "Invalid email or password"
    PAYMENT_PROCESSING_FAILED = "Payment processing failed"
    TRANSACTION_ALREADY_PROCESSED = "Transaction already processed"
    ORDER_NOT_FOUND = "Order not found"
    CART_NOT_FOUND = "Cart not found"
    CONFIGURATION_NOT_FOUND = "Configuration not found"
    CART_ITEM_NOT_FOUND = "Cart item not found"
    INVALID_ORDER_STATE_TRANSITION = "Invalid order state transition"
    PAYMENT_NOT_FOUND = "Payment not found"
    INVALID_WEBHOOK_SIGNATURE = "Invalid webhook signature"
    CATEGORY_NOT_FOUND = "Category not found"
    PRODUCT_NOT_FOUND = "Product not found"
    ACCESS_DENIED = "Access denied"