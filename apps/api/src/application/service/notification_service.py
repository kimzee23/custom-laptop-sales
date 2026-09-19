import logging
from typing import Dict, Any, Optional
from src.application.ports.inbound.notification_usecase import NotificationUseCase
from src.application.ports.outbound.notification_port import NotificationPort
from src.domain.model.notification import NotificationMessage, NotificationType

logger = logging.getLogger("notification_service")

class NotificationService(NotificationUseCase):
    def __init__(self, notification_port: NotificationPort):
        self.notification_port = notification_port

    async def send_verification_otp_email(self, email: str, name: str, otp: str) -> bool:
        subject = f"{otp} is your verification code - Custom Laptop Store"
        text_content = (
            f"Hello {name},\n\n"
            f"Your 6-digit verification code is: {otp}\n\n"
            f"This code will expire in 15 minutes. If you did not request this, please ignore this email.\n\n"
            f"Best regards,\nCustom Laptop Store Team"
        )
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Email Verification</title>
        </head>
        <body style="margin: 0; padding: 0; background-color: #0b0f19; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #e2e8f0;">
          <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #0b0f19; padding: 40px 10px;">
            <tr>
              <td align="center">
                <table role="presentation" width="100%" style="max-width: 560px; background-color: #131b2e; border-radius: 16px; border: 1px solid #1e293b; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
                  <!-- Header -->
                  <tr>
                    <td style="padding: 32px 32px 20px; background: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%); text-align: center;">
                      <h1 style="margin: 0; color: #ffffff; font-size: 24px; font-weight: 800; letter-spacing: -0.5px;">CUSTOM LAPTOP STORE</h1>
                      <p style="margin: 6px 0 0; color: #e0f2fe; font-size: 14px;">Verify Your Account</p>
                    </td>
                  </tr>
                  <!-- Body -->
                  <tr>
                    <td style="padding: 36px 32px;">
                      <h2 style="margin: 0 0 16px; color: #f8fafc; font-size: 20px; font-weight: 600;">Hello {name},</h2>
                      <p style="margin: 0 0 24px; color: #94a3b8; font-size: 15px; line-height: 1.6;">
                        Thank you for joining Custom Laptop Store. Use the 6-digit confirmation code below to verify your email address and activate your account:
                      </p>
                      
                      <!-- OTP Box -->
                      <div style="text-align: center; margin: 30px 0;">
                        <div style="display: inline-block; background: #0f172a; border: 2px solid #38bdf8; border-radius: 12px; padding: 18px 36px; box-shadow: 0 4px 20px rgba(56, 189, 248, 0.2);">
                          <span style="font-family: 'Courier New', Courier, monospace; font-size: 34px; font-weight: 800; letter-spacing: 10px; color: #38bdf8; display: block; text-shadow: 0 0 12px rgba(56, 189, 248, 0.4);">{otp}</span>
                        </div>
                      </div>

                      <p style="margin: 24px 0 0; color: #64748b; font-size: 13px; text-align: center; line-height: 1.5;">
                        ⏱️ This verification code is valid for <strong>15 minutes</strong>.<br>
                        If you did not request this registration, you can safely disregard this email.
                      </p>
                    </td>
                  </tr>
                  <!-- Footer -->
                  <tr>
                    <td style="padding: 20px 32px; background-color: #0b0f19; border-top: 1px solid #1e293b; text-align: center; color: #475569; font-size: 12px;">
                      &copy; 2026 Custom Laptop Store &bull; Empowering Custom Computing
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
        </body>
        </html>
        """

        msg = NotificationMessage(
            recipient_email=email,
            recipient_name=name,
            notification_type=NotificationType.EMAIL_VERIFICATION_OTP,
            subject=subject,
            html_content=html_content,
            text_content=text_content,
            metadata={"otp": otp}
        )
        return await self.notification_port.send_email(msg)

    async def send_order_confirmation_email(self, order_data: Dict[str, Any]) -> bool:
        email = order_data.get("customer_email") or ""
        name = order_data.get("customer_name") or "Valued Customer"
        order_number = order_data.get("order_number") or ""
        total_amount = f"₦{order_data.get('total_amount', 0.0):,.2f}"

        if not email:
            return False

        subject = f"Order Confirmed #{order_number} - Custom Laptop Store"
        text_content = (
            f"Hello {name},\n\n"
            f"Your order #{order_number} has been received!\n"
            f"Total Amount: {total_amount}\n"
            f"Status: {order_data.get('status', 'PENDING_PAYMENT')}\n\n"
            f"We are processing your custom build right away.\n"
            f"Best regards,\nCustom Laptop Store"
        )

        items = order_data.get("items", [])
        items_html = ""
        for it in items:
            p_name = it.get("title") or it.get("product_title") or "Custom Laptop Item"
            qty = it.get("quantity", 1)
            price = f"₦{it.get('total_price', 0.0):,.2f}"
            items_html += f"""
            <tr>
              <td style="padding: 12px 0; border-bottom: 1px solid #1e293b; color: #e2e8f0; font-size: 14px;">{p_name} &times; {qty}</td>
              <td style="padding: 12px 0; border-bottom: 1px solid #1e293b; color: #38bdf8; font-size: 14px; text-align: right; font-weight: 600;">{price}</td>
            </tr>
            """

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <body style="margin: 0; padding: 0; background-color: #0b0f19; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #e2e8f0;">
          <table width="100%" cellspacing="0" cellpadding="0" style="padding: 40px 10px;">
            <tr>
              <td align="center">
                <table width="100%" style="max-width: 580px; background-color: #131b2e; border-radius: 16px; border: 1px solid #1e293b; overflow: hidden;">
                  <tr>
                    <td style="padding: 28px; background: linear-gradient(135deg, #10b981 0%, #059669 100%); text-align: center;">
                      <h1 style="margin: 0; color: #ffffff; font-size: 22px; font-weight: 800;">ORDER RECEIVED</h1>
                      <p style="margin: 4px 0 0; color: #d1fae5; font-size: 14px;">Order #{order_number}</p>
                    </td>
                  </tr>
                  <tr>
                    <td style="padding: 32px;">
                      <h2 style="margin: 0 0 12px; color: #f8fafc; font-size: 18px;">Thank You, {name}!</h2>
                      <p style="margin: 0 0 20px; color: #94a3b8; font-size: 14px; line-height: 1.6;">
                        Your order has been placed successfully. Below is your order breakdown:
                      </p>
                      <table width="100%" cellspacing="0" cellpadding="0" style="margin-bottom: 24px;">
                        {items_html}
                        <tr>
                          <td style="padding: 16px 0 0; font-size: 16px; font-weight: bold; color: #f8fafc;">Total Paid:</td>
                          <td style="padding: 16px 0 0; font-size: 18px; font-weight: 800; color: #34d399; text-align: right;">{total_amount}</td>
                        </tr>
                      </table>
                      <div style="background: #0f172a; padding: 16px; border-radius: 8px; border-left: 4px solid #10b981; margin-top: 16px;">
                        <p style="margin: 0; color: #94a3b8; font-size: 13px;">Status: <strong style="color: #38bdf8;">{order_data.get('status', 'PENDING_PAYMENT')}</strong></p>
                      </div>
                    </td>
                  </tr>
                  <tr>
                    <td style="padding: 18px; background-color: #0b0f19; border-top: 1px solid #1e293b; text-align: center; color: #475569; font-size: 12px;">
                      &copy; 2026 Custom Laptop Store. All rights reserved.
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
        </body>
        </html>
        """

        msg = NotificationMessage(
            recipient_email=email,
            recipient_name=name,
            notification_type=NotificationType.ORDER_CONFIRMATION,
            subject=subject,
            html_content=html_content,
            text_content=text_content,
            metadata={"order_number": order_number}
        )
        return await self.notification_port.send_email(msg)

    async def send_payment_receipt_email(self, payment_data: Dict[str, Any], order_data: Optional[Dict[str, Any]] = None) -> bool:
        email = payment_data.get("customer_email") or (order_data.get("customer_email") if order_data else "")
        name = payment_data.get("customer_name") or (order_data.get("customer_name") if order_data else "Valued Customer")
        ref = payment_data.get("provider_reference") or payment_data.get("reference") or "N/A"
        amount = f"₦{payment_data.get('amount', 0.0):,.2f}"
        gateway = payment_data.get("provider") or "Online Gateway"

        if not email:
            return False

        subject = f"Official Payment Receipt: {amount} ({ref}) - Custom Laptop Store"
        text_content = (
            f"Dear {name},\n\n"
            f"We have received your payment of {amount} via {gateway}.\n"
            f"Payment Reference: {ref}\n"
            f"Status: SUCCESSFUL / PAID\n\n"
            f"Thank you for doing business with us!\n"
            f"Custom Laptop Store Team"
        )

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <body style="margin: 0; padding: 0; background-color: #0b0f19; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #e2e8f0;">
          <table width="100%" cellspacing="0" cellpadding="0" style="padding: 40px 10px;">
            <tr>
              <td align="center">
                <table width="100%" style="max-width: 560px; background-color: #131b2e; border-radius: 16px; border: 1px solid #1e293b; overflow: hidden;">
                  <tr>
                    <td style="padding: 28px; background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); text-align: center;">
                      <h1 style="margin: 0; color: #ffffff; font-size: 22px; font-weight: 800;">PAYMENT RECEIPT</h1>
                      <p style="margin: 4px 0 0; color: #ede9fe; font-size: 14px;">Transaction Verified</p>
                    </td>
                  </tr>
                  <tr>
                    <td style="padding: 32px;">
                      <h2 style="margin: 0 0 16px; color: #f8fafc; font-size: 18px;">Payment Successful!</h2>
                      <p style="margin: 0 0 24px; color: #94a3b8; font-size: 14px;">
                        Hello {name}, your transaction has been processed and verified.
                      </p>
                      
                      <div style="background: #0f172a; border-radius: 12px; padding: 20px; border: 1px solid #1e293b; margin-bottom: 24px;">
                        <table width="100%" cellspacing="0" cellpadding="6">
                          <tr>
                            <td style="color: #64748b; font-size: 13px;">Amount Paid:</td>
                            <td style="color: #34d399; font-size: 16px; font-weight: bold; text-align: right;">{amount}</td>
                          </tr>
                          <tr>
                            <td style="color: #64748b; font-size: 13px;">Payment Gateway:</td>
                            <td style="color: #e2e8f0; font-size: 13px; font-weight: 600; text-align: right; text-transform: uppercase;">{gateway}</td>
                          </tr>
                          <tr>
                            <td style="color: #64748b; font-size: 13px;">Reference:</td>
                            <td style="color: #94a3b8; font-family: monospace; font-size: 12px; text-align: right;">{ref}</td>
                          </tr>
                          <tr>
                            <td style="color: #64748b; font-size: 13px;">Status:</td>
                            <td style="color: #34d399; font-size: 13px; font-weight: bold; text-align: right;">CONFIRMED &bull; COMPLETED</td>
                          </tr>
                        </table>
                      </div>
                      <p style="margin: 0; color: #64748b; font-size: 12px; line-height: 1.5; text-align: center;">
                        This document serves as an electronic receipt for your records.
                      </p>
                    </td>
                  </tr>
                  <tr>
                    <td style="padding: 18px; background-color: #0b0f19; border-top: 1px solid #1e293b; text-align: center; color: #475569; font-size: 12px;">
                      &copy; 2026 Custom Laptop Store &bull; Official Payment Confirmation
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
        </body>
        </html>
        """

        msg = NotificationMessage(
            recipient_email=email,
            recipient_name=name,
            notification_type=NotificationType.PAYMENT_RECEIPT,
            subject=subject,
            html_content=html_content,
            text_content=text_content,
            metadata={"reference": ref, "amount": amount}
        )
        return await self.notification_port.send_email(msg)

    async def send_order_tracking_email(self, order_data: Dict[str, Any], tracking_status: str, tracking_note: Optional[str] = None) -> bool:
        email = order_data.get("customer_email") or ""
        name = order_data.get("customer_name") or "Valued Customer"
        order_number = order_data.get("order_number") or ""

        if not email:
            return False

        subject = f"Order #{order_number} Status Update: {tracking_status}"
        note_str = f"\nNote: {tracking_note}" if tracking_note else ""
        text_content = (
            f"Hello {name},\n\n"
            f"Your order #{order_number} has an updated status: {tracking_status}.{note_str}\n\n"
            f"You can track your order live from your customer dashboard.\n"
            f"Best regards,\nCustom Laptop Store"
        )

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <body style="margin: 0; padding: 0; background-color: #0b0f19; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #e2e8f0;">
          <table width="100%" cellspacing="0" cellpadding="0" style="padding: 40px 10px;">
            <tr>
              <td align="center">
                <table width="100%" style="max-width: 560px; background-color: #131b2e; border-radius: 16px; border: 1px solid #1e293b; overflow: hidden;">
                  <tr>
                    <td style="padding: 28px; background: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%); text-align: center;">
                      <h1 style="margin: 0; color: #ffffff; font-size: 22px; font-weight: 800;">ORDER TRACKING UPDATE</h1>
                      <p style="margin: 4px 0 0; color: #e0f2fe; font-size: 14px;">Order #{order_number}</p>
                    </td>
                  </tr>
                  <tr>
                    <td style="padding: 32px;">
                      <h2 style="margin: 0 0 14px; color: #f8fafc; font-size: 18px;">Status Update for {name}</h2>
                      <p style="margin: 0 0 20px; color: #94a3b8; font-size: 14px;">
                        The progress of your custom laptop order has been updated:
                      </p>
                      
                      <div style="background: #0f172a; border-radius: 12px; padding: 24px; text-align: center; border: 1px solid #1e293b;">
                        <span style="font-size: 13px; color: #64748b; text-transform: uppercase; letter-spacing: 1px;">Current Stage</span>
                        <div style="font-size: 22px; font-weight: 800; color: #38bdf8; margin: 8px 0;">{tracking_status}</div>
                        {f'<p style="margin: 8px 0 0; color: #94a3b8; font-size: 13px;">{tracking_note}</p>' if tracking_note else ''}
                      </div>
                    </td>
                  </tr>
                  <tr>
                    <td style="padding: 18px; background-color: #0b0f19; border-top: 1px solid #1e293b; text-align: center; color: #475569; font-size: 12px;">
                      &copy; 2026 Custom Laptop Store. Live Tracking Active.
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
        </body>
        </html>
        """

        msg = NotificationMessage(
            recipient_email=email,
            recipient_name=name,
            notification_type=NotificationType.ORDER_STATUS_UPDATE,
            subject=subject,
            html_content=html_content,
            text_content=text_content,
            metadata={"order_number": order_number, "status": tracking_status}
        )
        return await self.notification_port.send_email(msg)
