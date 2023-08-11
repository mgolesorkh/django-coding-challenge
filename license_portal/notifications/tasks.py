from celery import shared_task
from notifications.notifications import NotificationHandler
import logging

logger = logging.getLogger("celery")


@shared_task
def send_licence_expiration_notification_task() -> bool:
    try:
        notification_handler = NotificationHandler()
        notification_handler.send_license_expiration_notifications()
    except Exception as e:
        logger.error(str(e))
        return False
    return True
