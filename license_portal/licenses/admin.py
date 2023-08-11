from django.contrib import admin

from licenses.models import License, Client


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ["id", "package", "license_type", "client"]


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["id", "client_name"]
