from django.contrib import admin

from .models import Client, Path, PathRedirect, Request
from .tasks import block_clients_task, update_client_task


@admin.register(Path)
class PathAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name", "is_spam", "created_on")
    list_filter = ("is_spam", "created_on")
    readonly_fields = ("created_on",)
    actions = ["mark_as_spam", "mark_as_no_spam"]

    @admin.action(description="❗Mark as spam")
    def mark_as_spam(modeladmin, request, queryset):
        queryset.update(is_spam=True)

    @admin.action(description="✅ Mark as no spam")
    def mark_as_no_spam(modeladmin, request, queryset):
        queryset.update(is_spam=False)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "is_blocked", "user", "country", "site")
    readonly_fields = ("ip_address", "geoinfo", "user", "country", "site", "user_agent")
    list_filter = ("is_blocked", "site", "country")
    search_fields = ("ip_address", "site", "country")
    actions = ["block_ips", "update_values"]

    @admin.action(description="🚫 Block its IP Address")
    def block_ips(modeladmin, request, queryset):
        qs = queryset.filter(ip_address__isnull=False).exclude(
            ip_address=Client.DUMMY_IP_ADDRESS
        )
        block_clients_task(qs)

    @admin.action(description="🔄 Update values")
    def update_values(modeladmin, request, queryset):
        for client in queryset:
            update_client_task(client)


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    readonly_fields = tuple(field.name for field in Request._meta.fields)
    list_display = ("__str__", "client", "method", "status_code", "client__is_blocked")
    list_filter = ("ref", "status_code", "time", "method", "client__site")


@admin.register(PathRedirect)
class LinkRedirectAdmin(admin.ModelAdmin):
    list_display = ("__str__", "site", "from_path", "from_path")
    autocomplete_fields = ("from_path", "from_path")
