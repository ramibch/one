from django.conf import settings
from django.contrib import admin

from .models import Client, GeoInfo, Request
from .tasks import update_client_task


@admin.register(GeoInfo)
class GeoInfoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "city", "postal_code", "latitude")
    readonly_fields = tuple(field.name for field in GeoInfo._meta.fields)
    list_filter = ("is_in_european_union", "country_code", "time_zone")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "is_blocked", "user", "country", "site")
    readonly_fields = ("ip_address", "geoinfo", "user", "country", "site", "user_agent")
    list_filter = ("is_blocked", "request__path", "site", "country")
    search_fields = ("ip_address", "site", "country")
    actions = ["block_ips", "update_values"]

    @admin.action(description="🚫 Block its IPs")
    def block_ips(modeladmin, request, queryset):
        clients = queryset.filter(ip_address__isnull=False)
        new_ipaddrs = list(clients.values_list("ip_address", flat=True).distinct())
        path = settings.BASE_DIR / "nginx/conf.d/blockips.conf"
        actual_ipaddrs = [
            line.replace("deny ", "").replace(";", "")
            for line in path.read_text().split("\n")
            if len(line) > 6
        ]
        ips = set(new_ipaddrs) | set(actual_ipaddrs)
        output_text = "".join({f"deny {ip};\n" for ip in ips})
        path.write_text(output_text)
        clients.update(is_blocked=True)

    @admin.action(description="🔄 Update values")
    def update_values(modeladmin, request, queryset):
        for client in queryset:
            update_client_task(client)


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    readonly_fields = tuple(field.name for field in Request._meta.fields)
    list_display = ("__str__", "client", "method", "status_code", "client__is_blocked")
    list_filter = ("ref", "status_code", "method", "path", "time")
