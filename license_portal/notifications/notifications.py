from datetime import datetime
from typing import List, Any
from licenses.models import License
from dateutil.relativedelta import relativedelta
from django.core.mail import send_mail
from django.db.models import Q, Manager
from django.template import Template
from django.template.loader import get_template
from django.conf import settings

from notifications.models import Notification


class NotificationHandler:
    """
    Notification class to handle different type of notifications in system
    """

    def __init__(
        self,
        licence_model: Manager = License,
        template_path: str = "email/licenses_notification.html",
    ):
        """
        initial of notification handler class
        @param licence_model: related class model for licenses
        @type licence_model: Manager
        @param template_path: path to template of the notifications
        @type template_path: str
        """
        self.license_model = licence_model
        self.template_path = template_path

    def _get_weekday(self, datetime_value: datetime) -> int:
        """
        range 0-6 represent days of the week from monday
        @param datetime_value: requested datetime
        @type datetime_value: datetime
        @return: a number in range of 0 to 6
        @rtype:int
        """
        datetime_value.weekday()

    def _get_unexpired_licenses(self) -> Manager:
        """
        filter the queryset to remove all already expired licenses
        @return: filtered queryset
        @rtype: Manager
        """
        return self.license_model.objects.filter(
            expiration_datetime__gt=datetime.utcnow().astimezone()
        )

    def _apply_expire_license_rules(self) -> Manager:
        """
        apply all rules related to license expiration notification
        @return: a filtered queryset
        @rtype: Manager
        """
        timezone_now = datetime.now().astimezone()
        queryset = self._get_unexpired_licenses()

        # rule: licenses that will expire in exact 4 monthes
        filter_condition = Q(
            expiration_datetime__date=(timezone_now + relativedelta(months=4)).date()
        )
        # rule: licenses that will expire within a week
        filter_condition |= Q(
            expiration_datetime__lt=timezone_now + relativedelta(weeks=1)
        )
        # rule: licenses that will expire within a month in condition that this code run on monday
        if self._get_weekday(timezone_now) == 0:
            filter_condition |= Q(
                expiration_datetime__lt=timezone_now + relativedelta(months=1)
            )
        return queryset.filter(filter_condition)

    def _process_licenses_notification_data(self, licenses_data_rows: list) -> dict:
        """
        this step will form the query data to context that templates needs to fill the params
        @param licenses_data_rows: license data rows from queryset values
        @type licenses_data_rows: list
        @return: processed dictionary for template context
        @rtype: dict
        """
        result = dict()
        license_types = dict(License.LicenseType.choices)
        license_packages = dict(License.Package.choices)
        for notification_data_row in licenses_data_rows:
            notification_data_row["license_type"] = license_types[
                notification_data_row["license_type"]
            ]
            notification_data_row["package"] = license_packages[
                notification_data_row["package"]
            ]
            result.setdefault(
                notification_data_row.get("client__admin_poc__email"), []
            ).append(notification_data_row)
        return result

    def _get_licenses_contexts(self) -> dict:
        """
        prepare processed data for template context
        @return: context dictionary
        @rtype: dict
        """
        needed_fields = [
            "id",
            "license_type",
            "package",
            "expiration_datetime",
            "client__admin_poc__email",
            "client__poc_contact_name",
            "client__poc_contact_email",
        ]
        licenses_data_rows = list(
            self._apply_expire_license_rules().values(*needed_fields)
        )
        return self._process_licenses_notification_data(licenses_data_rows)

    def send_license_expiration_notifications(self) -> Notification:
        """
        use db and rules for prepare and send all notifications related to license expiration
        @return: notification object
        @rtype: Notification
        """
        email_notification = EmailNotification(
            template_path=self.template_path, subject="License Expiration Alert"
        )
        licenses_contexts = self._get_licenses_contexts()
        notification = Notification.objects.create(total_count=len(licenses_contexts))

        for email_address, context in licenses_contexts.items():
            context = {"licenses": context}

            email_notification.send_notification(
                recipients=[email_address], context=context, notification=notification
            )
        return notification


class EmailNotification:
    """A convenience class to send email notifications"""

    def __init__(
        self,
        template_path: str,
        from_email: str = settings.DEFAULT_FROM_EMAIL,
        subject: str = None,
    ):
        """
        initial Email notification
        @param template_path: path for template of email
        @type template_path: str
        @param from_email: email address for from value
        @type from_email: str
        @param subject: subject for default subject of all notifications
        @type subject: str
        """
        self.template_path = template_path
        self.from_email = from_email
        self.subject = subject

    def load_template(self) -> Template:
        """Load the configured template path"""
        return get_template(self.template_path)

    def send_notification(
        self, recipients: List[str], notification, context: Any, subject: str = None
    ) -> bool:
        """
        Send the notification using the given context
        @param recipients:list of emails
        @type recipients: list
        @param notification: notification object to use for log items
        @type notification: Notification
        @param context: context to pass to template
        @type context: str
        @param subject: subject of email
        @type subject: str
        @return: result
        @rtype: bool
        """
        template = self.load_template()
        message_body = template.render(context=context)
        try:
            send_mail(
                subject or self.subject,
                message_body,
                self.from_email,
                recipients,
                fail_silently=False,
            )
            send_res = True
        except Exception as e:
            send_res = False
            # todo: log related error
        notification.items.create(
            subject=subject or self.subject,
            body=message_body,
            endpoint=",".join(recipients),
            notification=notification,
            is_successful=True if send_res else False,
        )
        return send_res
