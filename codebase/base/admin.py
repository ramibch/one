from django.contrib import admin
from django.db.migrations.recorder import MigrationRecorder
from django.utils.timezone import now


@admin.register(MigrationRecorder.Migration)
class MigrationRecorderAdmin(admin.ModelAdmin):
    list_display = ("name", "app", "applied")
    list_filter = ("app", "applied")
    actions = ("set_applied_now",)

    @admin.action(description="Set applied now | ⚠️ You must know what you are doing!")
    def set_applied_now(modeladmin, request, queryset):
        queryset.update(applied=now())
