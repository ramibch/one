from django.contrib import admin
from django.db.migrations.recorder import MigrationRecorder

from .models import Traffic


@admin.register(MigrationRecorder.Migration)
class MigrationRecorderAdmin(admin.ModelAdmin):
    list_display = ("name", "app", "applied")
    list_filter = ("app", "applied")


@admin.register(Traffic)
class TrafficAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "request_path",
        "response_status_code",
        "request_method",
        "user",
    )
    list_filter = ("time", "site", "request_method", "response_status_code")
    readonly_fields = (
        "request_GET",
        "request_GET_ref",
        "request_POST",
        "request_path",
        "request_headers",
        "request_country_code",
        "response_headers",
        "response_status_code",
        "request_method",
        "user",
        "site",
        "time",
    )
