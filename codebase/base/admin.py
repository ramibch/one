from django.contrib import admin
from django.db.migrations.recorder import MigrationRecorder
from django.utils.timezone import now
from huey.contrib.djhuey import HUEY

from .models import ExtendedSite


@admin.register(MigrationRecorder.Migration)
class MigrationRecorderAdmin(admin.ModelAdmin):
    list_display = ("name", "app", "applied")
    list_filter = ("app", "applied")
    actions = ("set_applied_now",)

    @admin.action(description="Set applied now | ⚠️ You must know what you are doing!")
    def set_applied_now(modeladmin, request, queryset):
        queryset.update(applied=now())


@admin.register(ExtendedSite)
class ExtendedSiteAdmin(admin.ModelAdmin):
    list_display = ("__str__", "site__domain", "site__name")
    search_fields = ("site__domain", "site__name")
    readonly_fields = ("last_huey_flush",)
    # list_editable = ("site__domain", "site__name")
    actions = ["flush_huey"]

    def flush_huey(modeladmin, request, queryset):
        HUEY.flush()
        queryset.update(last_huey_flush=now())
