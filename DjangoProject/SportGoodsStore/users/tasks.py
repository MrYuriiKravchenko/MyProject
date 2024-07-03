import logging
from celery import shared_task
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

@shared_task
def send_email_task(subject, message, from_email, recipient_list, **kwargs):
    try:
        send_mail(subject, message, from_email, recipient_list, **kwargs)
        logger.info(f"Email sent to {recipient_list}")
    except Exception as e:
        logger.error(f"Failed to send email to {recipient_list}: {e}")
        raise e
