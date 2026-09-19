import asyncio
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.application.ports.outbound.notification_port import NotificationPort
from src.domain.model.notification import NotificationMessage
from src.infrastructure.config.settings import settings

logger = logging.getLogger("notification_service")

class SmtpEmailAdapter(NotificationPort):
    """
    100% Free SMTP Email Adapter (Gmail SMTP, Brevo, standard SMTP, or local fallback).
    Executes SMTP dispatch in a background worker thread so the async event loop is not blocked.
    If credentials are missing or network fails, logs cleanly and succeeds gracefully.
    """

    def __init__(self):
        self.host = settings.SMTP_HOST
        self.port = settings.SMTP_PORT
        self.user = settings.SMTP_USER
        self.password = settings.SMTP_PASSWORD
        self.from_email = settings.SMTP_FROM_EMAIL or self.user or "noreply@customlaptopstore.com"
        self.use_tls = settings.SMTP_USE_TLS

    async def send_email(self, message: NotificationMessage) -> bool:
        # If credentials are not configured, log to console for development / zero-cost operation
        if not self.user or not self.password:
            logger.warning(
                f"[NOTIFICATION DISPATCH - SIMULATED / ZERO-COST FALLBACK]\n"
                f"To: {message.recipient_email} ({message.recipient_name})\n"
                f"Subject: {message.subject}\n"
                f"Type: {message.notification_type}\n"
                f"Metadata: {message.metadata}\n"
                f"Note: Set SMTP_USER and SMTP_PASSWORD in your environment (e.g. free Gmail App Password) for live inbox delivery."
            )
            return True

        # Dispatch via thread to keep FastAPI non-blocking
        try:
            return await asyncio.to_thread(self._sync_send_email, message)
        except Exception as e:
            logger.error(f"[NOTIFICATION ERROR] Failed to send email to {message.recipient_email}: {e}")
            # Graceful resilience: log and continue so customer actions never fail
            return False

    def _sync_send_email(self, message: NotificationMessage) -> bool:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = message.subject
        msg["From"] = f"Custom Laptop Store <{self.from_email}>"
        msg["To"] = f"{message.recipient_name} <{message.recipient_email}>"

        if message.text_content:
            part1 = MIMEText(message.text_content, "plain", "utf-8")
            msg.attach(part1)

        part2 = MIMEText(message.html_content, "html", "utf-8")
        msg.attach(part2)

        server = None
        try:
            server = smtplib.SMTP(self.host, self.port, timeout=10)
            if self.use_tls:
                server.starttls()
            server.login(self.user, self.password)
            server.sendmail(self.from_email, [message.recipient_email], msg.as_string())
            logger.info(f"[EMAIL SENT] Successfully delivered '{message.subject}' to {message.recipient_email}")
            return True
        finally:
            if server:
                try:
                    server.quit()
                except Exception:
                    pass
