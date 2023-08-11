from unittest.mock import patch

from django.test import TestCase
from datetime import datetime

from licenses.models import License
from dateutil.relativedelta import relativedelta

from notifications.notifications import NotificationHandler


class TestLicenseExpirationNotification(TestCase):
    """
    test class for rules of notification for license expiration
    """

    fixtures = ["sample_data/sample_data_fixture"]

    @patch("notifications.notifications.NotificationHandler._get_weekday")
    def test_expire_license_notification_rules(self, weekday_mock: any) -> None:
        """
        this test will cover all rules.
        in sample data wwe have 4 client and each client has 5 licenses.
        @param weekday_mock: mock of weekday to test monday from other days
        @type weekday_mock: any
        """
        notification_handler = NotificationHandler()

        # set weekday to a day not equal to monday that is 0
        weekday_mock.return_value = 1
        now_datetime = datetime.now().astimezone()

        # expire all licenses
        License.objects.update(expiration_datetime=now_datetime - relativedelta(days=1))

        # test notification instance to run but not send any notif because all licenses are expired already
        notification = notification_handler.send_license_expiration_notifications()
        self.assertEqual(notification.items.count(), notification.total_count)
        self.assertEqual(notification.total_count, 0)

        # update all licenses related to client c1 to rule number 1
        License.objects.filter(client__client_name="c1").update(
            expiration_datetime=now_datetime + relativedelta(months=4)
        )

        # update all licenses related to client c1 to rule number 2
        License.objects.filter(client__client_name="c2").update(
            expiration_datetime=now_datetime + relativedelta(days=6)
        )

        # update all licenses related to client c1 to rule number 3
        License.objects.filter(client__client_name="c3").update(
            expiration_datetime=now_datetime + relativedelta(months=1)
        )

        # check all notification items in the case it is not monday
        notification = notification_handler.send_license_expiration_notifications()
        self.assertEqual(notification.items.count(), notification.total_count)
        self.assertEqual(notification.total_count, 2)

        # check all notification items in the case it is  monday
        weekday_mock.return_value = 0
        notification = notification_handler.send_license_expiration_notifications()
        self.assertEqual(notification.items.count(), notification.total_count)
        self.assertEqual(notification.total_count, 3)
