from django.contrib import admin

from notifications.models import Notification, NotificationItem


@admin.register(Notification)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ["id", "notification_type", "created_datetime"]


@admin.register(NotificationItem)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["id", "endpoint", "notification_channel", "created_datetime"]
