from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from notifications.api.serializers import (
    NotificationSerializer,
    NotificationItemSerializer,
)
from notifications.models import Notification, NotificationItem


class NotificationHistoryViewset(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet
):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["notification_type"]


class NotificationItemViewset(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet
):
    queryset = NotificationItem.objects.all()
    serializer_class = NotificationItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["notification_id", "endpoint"]
