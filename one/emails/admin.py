from django.contrib import admin

from .models import (
    Attachment,
    DomainDNSError,
    MessageSent,
    MessageTemplate,
    Sender,
    TemplateRecipient,
)
from .tasks import task_send_email_templates


class EmailRecipientInline(admin.TabularInline):
    model = TemplateRecipient
    extra = 5
    exclude = ("subject", "body")
    readonly_fields = ("email_sent",)


class EmailAttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0


@admin.register(Sender)
class SenderAdmin(admin.ModelAdmin):
    search_fields = ("name", "address")
    list_display = ("__str__", "name", "address")


@admin.register(MessageTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    search_fields = ("body", "subject")
    autocomplete_fields = ("sender",)
    inlines = (EmailAttachmentInline, EmailRecipientInline)
    actions = ("send_emails",)

    @admin.action(description="📧 Send Emails")
    def send_emails(modeladmin, request, queryset):
        task_send_email_templates(queryset)


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
