""" Data model for licenses application
"""
from datetime import timedelta, datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

LICENSE_EXPIRATION_DELTA = timedelta(days=90)


def get_default_license_expiration() -> datetime:
    """Get the default expiration datetime"""
    return datetime.utcnow() + LICENSE_EXPIRATION_DELTA


class License(models.Model):
    """Data model for a client license allowing access to a package"""

    class LicenseType(models.IntegerChoices):
        PRODUCTION = 0, _("production")
        EVALUATION = 1, _("evaluation")

    class Package(models.IntegerChoices):
        JAVASCRIPT_SDK = 0, _("javascript sdk")
        IOS_SDK = 1, _("ios sdk")
        ANDROID_SDK = 2, _("android sdk")

    client = models.ForeignKey("Client", on_delete=models.CASCADE)
    package = models.PositiveSmallIntegerField(choices=Package.choices)
    license_type = models.PositiveSmallIntegerField(choices=LicenseType.choices)

    created_datetime = models.DateTimeField(auto_now=True)
    expiration_datetime = models.DateTimeField(default=get_default_license_expiration)

    def __str__(self):
        return str(self.id)


class Client(models.Model):
    """A client who holds licenses to packages"""

    client_name = models.CharField(max_length=120, unique=True)
    poc_contact_name = models.CharField(max_length=120)
    poc_contact_email = models.EmailField()

    admin_poc = models.ForeignKey(
        User, limit_choices_to={"is_staff": True}, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.client_name
