from django.contrib import admin

from .models import (
    PostalDomainDNSError,
    PostalMessage,
    PostalReplyMessage,
    Sender,
    TemplateAttachment,
    TemplateMessage,
    TemplateRecipient,
)
from .tasks import task_send_email_templates


class RecipientInline(admin.TabularInline):
    model = TemplateRecipient
    extra = 5
    exclude = ("subject", "body")
    readonly_fields = ("send_times",)


class AttachmentInline(admin.TabularInline):
    model = TemplateAttachment
    extra = 0


@admin.register(TemplateAttachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "email")
    search_fields = ("email", "file")


@admin.register(TemplateRecipient)
class RecipientAdmin(admin.ModelAdmin):
    search_fields = ("to_address", "var_1", "var_2", "var_3")
    list_display = ("__str__", "email", "draft", "send_times", "sent_on")
    list_filter = ("email", "draft", "send_times")
    readonly_fields = ("email", "send_times", "sent_on")
    actions = ["reset_send_times", "mark_as_draft", "mark_as_no_draft"]

    @admin.action(description="0️⃣ Reset send times")
    def reset_send_times(modeladmin, request, queryset):
        queryset.update(send_times=0)

    @admin.action(description="✏️ Mark as draft")
    def mark_as_draft(modeladmin, request, queryset):
        queryset.update(draft=True)

    @admin.action(description="✅ Mark as no draft")
    def mark_as_no_draft(modeladmin, request, queryset):
        queryset.update(draft=False)


@admin.register(Sender)
class SenderAdmin(admin.ModelAdmin):
    search_fields = ("name", "address")
    list_display = ("__str__", "name", "address")


@admin.register(TemplateMessage)
class EmailMessageTemplateAdmin(admin.ModelAdmin):
    search_fields = ("body", "subject")
    autocomplete_fields = ("sender",)
    inlines = (AttachmentInline, RecipientInline)
    actions = ("send_emails",)
    list_display = ("subject", "body", "sender", "reply_to", "cc")
    list_filter = ("is_periodic", "sender")

    @admin.action(description="📧 Send Emails")
    def send_emails(modeladmin, request, queryset):
        task_send_email_templates(queryset)


@admin.register(PostalDomainDNSError)
class DomainDNSErrorAdmin(admin.ModelAdmin):
    list_display = (
        "domain",
        "spf_status",
        "dkim_status",
        "mx_status",
        "return_path_status",
    )
    list_filter = ("domain",)
    readonly_fields = tuple(field.name for field in PostalDomainDNSError._meta.fields)


class PostalReplyMessageInline(admin.TabularInline):
    model = PostalReplyMessage
    extra = 1
    max_num = 1
    readonly_fields = ("replied", "replied_on")


@admin.register(PostalMessage)
class PostalMessageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "mail_from", "mail_to", "direction", "url")
    list_filter = ("status", "tag", "spam_status", "direction")
    readonly_fields = ["url"] + [field.name for field in PostalMessage._meta.fields]
    inlines = [PostalReplyMessageInline]
