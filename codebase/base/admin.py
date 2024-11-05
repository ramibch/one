from django.contrib import admin
from django.contrib.sites.models import Site
from django.db.migrations.recorder import MigrationRecorder
from django.utils.timezone import now
from huey.contrib.djhuey import HUEY

from .models import Website


@admin.register(MigrationRecorder.Migration)
class MigrationRecorderAdmin(admin.ModelAdmin):
    list_display = ("name", "app", "applied")
    list_filter = ("app", "applied")
    actions = ("set_applied_now",)

    @admin.action(description="Set applied now | ⚠️ You must know what you are doing!")
    def set_applied_now(modeladmin, request, queryset):
        queryset.update(applied=now())


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    # Unregister Django Site Model
    admin.site.unregister(Site)

    list_display = ("__str__", "domain", "name")
    search_fields = ("domain", "name")
    list_editable = ("domain", "name")
    actions = ["flush_huey"]

    def flush_huey(modeladmin, request, queryset):
        HUEY.flush()
        queryset.update(last_huey_flush=now())
