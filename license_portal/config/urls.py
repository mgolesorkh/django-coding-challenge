from django.contrib import admin
from django.urls import path
from rest_framework import routers

from notifications.api.views import NotificationHistoryViewset, NotificationItemViewset

from notifications.views import (
    LicenseExpirationNotificationView,
    NotificationHistoryView,
    NotificationItemsView,
    NotificationItemBodyView,
    HomeView,
)

router = routers.SimpleRouter()
router.register(
    r"api/notifications", NotificationHistoryViewset, basename="notification"
)
router.register(
    r"api/notification_items", NotificationItemViewset, basename="notification_item"
)
urlpatterns = [
    path(r"admin/", admin.site.urls),
    path(
        r"notifications/license_expiration/",
        LicenseExpirationNotificationView.as_view(),
    ),
    path(r"", HomeView.as_view()),
    path(
        r"notifications/history/",
        NotificationHistoryView.as_view(),
        name="notification_history",
    ),
    path(
        r"notifications/history/<int:notification_id>/items/",
        NotificationItemsView.as_view(),
        name="notification_items",
    ),
    path(
        r"notifications/items/<int:notification_item_id>/body/",
        NotificationItemBodyView.as_view(),
        name="notification_item_body",
    ),
]
urlpatterns += router.urls
