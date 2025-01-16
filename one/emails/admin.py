from django.contrib import admin

from .models import DomainDNSError, MessageSent


@admin.register(DomainDNSError)
class DomainDNSErrorAdmin(admin.ModelAdmin):
    list_display = (
        "domain",
        "spf_status",
        "dkim_status",
        "mx_status",
        "return_path_status",
    )
    list_filter = ("domain",)
    readonly_fields = tuple(field.name for field in DomainDNSError._meta.fields)


@admin.register(MessageSent)
class MessageSentAdmin(admin.ModelAdmin):
    list_filter = ("status", "message_tag", "message_spam_status", "message_direction")
    readonly_fields = tuple(field.name for field in MessageSent._meta.fields)
    list_display = ("message_id", "message_to", "message_from", "output")
