from django.db import models
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):
    """A client who holds licenses to packages"""

    class NotificationType(models.IntegerChoices):
        LICENSE_EXPIRATION_TYPE = 1, _("license expiration")

    notification_type = models.PositiveSmallIntegerField(
        choices=NotificationType.choices,
        default=NotificationType.LICENSE_EXPIRATION_TYPE,
    )
    total_count = models.PositiveIntegerField(default=0)
    created_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_datetime",)

    def __str__(self) -> str:
        return str(self.id)

    @property
    def sent_count(self) -> int:
        return self.items.filter(is_successful=True).count()


class NotificationItem(models.Model):
    """A client who holds licenses to packages"""

    class ChannelType(models.IntegerChoices):
        EMAIL_NOTIFICATION = 1, _("email")
        SMS_NOTIFICATION = 2, _("sms")

    notification_channel = models.PositiveSmallIntegerField(
        choices=ChannelType.choices, default=ChannelType.EMAIL_NOTIFICATION
    )
    subject = models.CharField(max_length=300)
    body = models.TextField()
    endpoint = models.CharField(max_length=150)
    created_datetime = models.DateTimeField(auto_now=True)
    notification = models.ForeignKey(
        Notification, on_delete=models.PROTECT, related_name="items"
    )
    is_successful = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_datetime",)

    def __str__(self) -> str:
        return str(self.id)
