from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_notification_email(to_email, subject, template, context):
    """Send a notification email using a template."""
    try:
        message = render_to_string(template, context)
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to_email],
            fail_silently=False,
        )
        logger.info(f'Email sent to {to_email}: {subject}')
    except Exception as e:
        logger.error(f'Failed to send email to {to_email}: {e}')
