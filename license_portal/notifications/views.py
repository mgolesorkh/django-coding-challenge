from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.views import APIView, Response

from notifications.models import Notification, NotificationItem
from notifications.tasks import send_licence_expiration_notification_task


class LicenseExpirationNotificationView(APIView):
    def post(self, **kwargs) -> HttpResponse:
        send_licence_expiration_notification_task.apply_async()
        return Response(status=200)


class HomeView(View):
    def get(self, **kwargs) -> HttpResponse:
        return redirect("notification_history")


class NotificationHistoryView(View):
    def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        context = {"notifications": Notification.objects.all()}
        return render(request, "notification_history.html", context=context)


class NotificationItemsView(View):
    def get(self, request: HttpRequest, notification_id: int, **kwargs) -> HttpResponse:
        notification = get_object_or_404(Notification, id=notification_id)
        context = {"notification": notification}

        return render(request, "notification_items.html", context=context)


class NotificationItemBodyView(View):
    def get(
        self, request: HttpRequest, notification_item_id: int, **kwargs
    ) -> HttpResponse:
        notification_item = get_object_or_404(NotificationItem, id=notification_item_id)
        context = {"content": notification_item.body}
        return render(request, "notification_item_body.html", context=context)
