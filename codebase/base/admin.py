from django.conf import settings
from django.contrib import admin
from django.db.migrations.recorder import MigrationRecorder
from modeltranslation.admin import TranslationAdmin

from .models import Topic, Traffic
from .utils.actions import translation_actions


@admin.register(MigrationRecorder.Migration)
class MigrationRecorderAdmin(admin.ModelAdmin):
    list_display = ("name", "app", "applied")
    list_filter = ("app", "applied")


@admin.register(Topic)
class TopicAdmin(TranslationAdmin):
    actions = translation_actions


@admin.register(Traffic)
class TrafficAdmin(admin.ModelAdmin):
    list_display = ("__str__", "ip", "ip_blocked", "status_code", "method", "user")
    list_filter = ("path", "site", "ip_blocked", "status_code", "method", "time")
    readonly_fields = (
        "get",
        "ref",
        "post",
        "path",
        "headers",
        "ip",
        "country_code",
        "status_code",
        "method",
        "user",
        "site",
        "time",
    )

    actions = ["block_ips"]

    @admin.action(description="🕵 Block its IPs")
    def block_ips(modeladmin, request, queryset):
        traffic_objs = queryset.filter(ip__isnull=False)
        new_ips = list(traffic_objs.values_list("ip", flat=True).distinct())
        path = settings.BASE_DIR / "nginx/conf.d/blockips.conf"
        actual_ips = [
            line.replace("deny ", "").replace(";", "")
            for line in path.read_text().split("\n")
            if len(line) > 6
        ]
        ips = set(new_ips) | set(actual_ips)
        output_text = "".join({f"deny {ip};\n" for ip in ips})
        path.write_text(output_text)
        traffic_objs.update(ip_blocked=True)
