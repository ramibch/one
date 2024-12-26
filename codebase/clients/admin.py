from django.contrib import admin

from .models import Client, GeoInfo, Request, SpamPath
from .tasks import block_clients_task, update_client_task


@admin.register(SpamPath)
class SpamPathAdmin(admin.ModelAdmin):
    list_display = ("name", "created_on")
    readonly_fields = ("created_on",)


@admin.register(GeoInfo)
class GeoInfoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "city", "postal_code", "latitude", "longitude")
    readonly_fields = tuple(field.name for field in GeoInfo._meta.fields)
    list_filter = ("is_in_european_union", "country_code", "time_zone")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "is_blocked", "user", "country", "site")
    readonly_fields = ("ip_address", "geoinfo", "user", "country", "site", "user_agent")
    list_filter = ("is_blocked", "request__path", "site", "country")
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
    list_filter = ("ref", "status_code", "method", "client__site", "path", "time")
    actions = ["make_paths_autoblock"]

    @admin.action(description="❗Create auto block paths from these")
    def make_paths_autoblock(modeladmin, request, queryset):
        paths = list(queryset.distinct().values_list("path", flat=True))
        auto_block_paths = []
        for path in paths:
            auto_block_paths.append(SpamPath(name=path))
        SpamPath.objects.bulk_create(auto_block_paths, ignore_conflicts=True)
