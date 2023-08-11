from rest_framework import serializers

from notifications.models import Notification, NotificationItem


class NotificationSerializer(serializers.ModelSerializer):
    notification_type_text = serializers.CharField(
        source="get_notification_type_display", read_only=True
    )

    class Meta:
        model = Notification
        fields = [
            "id",
            "notification_type",
            "total_count",
            "sent_count",
            "created_datetime",
            "notification_type_text",
        ]


class NotificationItemSerializer(serializers.ModelSerializer):
    notification_channel_text = serializers.CharField(
        source="get_notification_channel_display", read_only=True
    )

    class Meta:
        model = NotificationItem
        fields = [
            "id",
            "notification_channel",
            "subject",
            "body",
            "endpoint",
            "created_datetime",
            "notification_channel_text",
            "is_successful",
        ]
