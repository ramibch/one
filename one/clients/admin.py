from django.contrib import admin

from one.admin import OneModelAdmin

from .models import Client, Path, PathRedirect, Request
from .tasks import block_spammy_clients


@admin.register(Path)
class PathAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name", "is_spam", "created_at")
    list_filter = ("is_spam", "created_at")
    actions = ["mark_as_spam", "mark_as_no_spam"]

    @admin.action(description="❗Mark as spam")
    def mark_as_spam(modeladmin, request, queryset):
        queryset.update(is_spam=True)

    @admin.action(description="✅ Mark as no spam")
    def mark_as_no_spam(modeladmin, request, queryset):
        queryset.update(is_spam=False)


class RequestInline(admin.StackedInline):
    model = Request
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "emoji", "is_blocked", "user", "country")
    list_filter = ("is_blocked", "is_bot", "country")
    search_fields = ("ip_address", "country")
    actions = ["block_ips", "update_values"]
    list_select_related = ("user", "geoinfo")
    inlines = (RequestInline,)

    @admin.action(description="🚫 Block its IP Address")
    def block_ips(modeladmin, request, queryset):
        qs = queryset.filter(ip_address__isnull=False).exclude(
            ip_address=Client.DUMMY_IP_ADDRESS
        )
        block_spammy_clients(qs)

    @admin.action(description="🔄 Update values")
    def update_values(modeladmin, request, queryset):
        for client in queryset:
            client.update_geo_values()


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    readonly_fields = tuple(field.name for field in Request._meta.fields)
    list_display = ("__str__", "client", "method", "status_code", "client__is_blocked")
    list_filter = (
        "client__is_bot",
        "status_code",
        "method",
        "time",
        "ref",
    )
    search_fields = ("path__name", "client__ip_address")


@admin.register(PathRedirect)
class LinkRedirectAdmin(OneModelAdmin):
    list_display = ("__str__", "from_path", "to_path")
    autocomplete_fields = ("from_path", "to_path")
