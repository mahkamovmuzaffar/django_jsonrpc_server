from django.core.mail import send_mail, EmailMessage
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send(to_email: str, subject: str, message: str, html_message: str = None, from_email: str = None) -> bool:
    """
    Sends an email using Django's email backend.

    Args:
        to_email (str): Recipient's email address.
        subject (str): Email subject line.
        message (str): Plain text version of the message.
        html_message (str, optional): Optional HTML version of the message.
        from_email (str, optional): Sender's email. Defaults to settings.DEFAULT_FROM_EMAIL.

    Returns:
        bool: True if sent successfully, False otherwise.
    """
    from_email = from_email or settings.DEFAULT_FROM_EMAIL

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[to_email],
            fail_silently=False,
            html_message=html_message,
        )
        logger.info(f"Email sent to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        return False
