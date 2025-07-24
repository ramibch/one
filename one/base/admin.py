from django.contrib import admin
from django.contrib.sessions.models import Session
from django.db.migrations.recorder import MigrationRecorder
from django.http import HttpResponse

from one.admin import OneTranslatableModelAdmin
from one.emails.models import ReplyMessage

from .models import Animation, ContactMessage, CSPReport, Link, SearchTerm


@admin.register(Link)
class LinkAdmin(OneTranslatableModelAdmin):
    list_display = ("__str__", "url_path", "topic", "external_url")
    list_editable = ("url_path", "topic", "external_url")
    search_fields = ("topic", "url_path", "external_url")


@admin.register(Animation)
class AnimationAdmin(admin.ModelAdmin):
    list_display = ("animation_type", "name", "repeat", "speed", "delay")


@admin.register(MigrationRecorder.Migration)
class MigrationRecorderAdmin(admin.ModelAdmin):
    list_display = ("name", "app", "applied")
    list_filter = ("app", "applied")


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("session_key", "expire_date")
    list_filter = ("expire_date",)
    readonly_fields = ("session_key", "session_data", "expire_date")


@admin.register(SearchTerm)
class SearchTermAdmin(admin.ModelAdmin):
    list_display = ("query", "site", "client", "created_at")
    readonly_fields = ("query", "site", "client", "created_at")
    list_filter = ("site", "created_at")

    def has_add_permission(self, request):
        return False


class ReplyMessageInline(admin.TabularInline):
    model = ReplyMessage
    extra = 1
    max_num = 1
    readonly_fields = ("replied", "replied_on")
    exclude = ("postal_message",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "message", "client", "client__is_blocked")
    list_filter = ("client__is_blocked", "site", "created_at")
    readonly_fields = tuple(field.name for field in ContactMessage._meta.fields)
    inlines = [ReplyMessageInline]


@admin.register(CSPReport)
class CSPReportAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "violated_directive",
        "effective_directive",
        "blocked_uri",
        "document_uri",
        "source_file",
        "status_code",
    )
    list_filter = (
        "violated_directive",
        "effective_directive",
        "disposition",
        "status_code",
        "created_at",
    )
    search_fields = (
        "blocked_uri",
        "document_uri",
        "source_file",
        "referrer",
        "original_policy",
    )
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    readonly_fields = tuple(f.name for f in CSPReport._meta.fields)

    actions = ["export_csp_violations_as_txt"]

    @admin.action(description="Export selected CSP violations as .txt")
    def export_csp_violations_as_txt(modeladmin, request, queryset):
        response = HttpResponse(content_type="text/plain")
        response["Content-Disposition"] = 'attachment; filename="csp_violations.txt"'

        lines = []
        for obj in queryset:
            lines.append("===")
            lines.append(f"Violated Directive: {obj.violated_directive}")
            lines.append(f"Effective Directive: {obj.effective_directive}")
            lines.append(f"Blocked URI:        {obj.blocked_uri}")
            lines.append(f"Document URI:       {obj.document_uri}")
            lines.append(f"Source File:        {obj.source_file}")
            lines.append(f"Line: {obj.line_number}, Column: {obj.column_number}")
            lines.append(f"Status Code:        {obj.status_code}")
            lines.append(f"Referrer:           {obj.referrer}")
            lines.append("")

        response.write("\n".join(lines))
        return response
