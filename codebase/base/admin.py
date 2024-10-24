from django.contrib import admin
from django.db.migrations.recorder import MigrationRecorder
from django.utils.timezone import now

from .models import MenuItem, PageLink


@admin.register(MigrationRecorder.Migration)
class MigrationRecorderAdmin(admin.ModelAdmin):
    list_display = ("name", "app", "applied")
    list_filter = ("app", "applied")
    actions = ("set_applied_now",)

    @admin.action(description="Set applied now | ⚠️ You must know what you are doing!")
    def set_applied_now(modeladmin, request, queryset):
        queryset.update(applied=now())


class PageLinkInline(admin.TabularInline):
    model = PageLink
    extra = 3


@admin.register(MenuItem)
class NavbarItemAdmin(admin.ModelAdmin):
    list_display = ("title", "show_in_navbar", "show_in_footer")
    list_filter = ("show_in_navbar", "show_in_footer")
    inlines = (PageLinkInline,)
