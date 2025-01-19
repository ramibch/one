from django.contrib import admin

from .models import (
    Attachment,
    DomainDNSError,
    EmailMessageTemplate,
    PostalMessage,
    Recipient,
    Sender,
)
from .tasks import task_send_email_templates


class RecipientInline(admin.TabularInline):
    model = Recipient
    extra = 5
    exclude = ("subject", "body")
    readonly_fields = ("send_times",)


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    search_fields = ("to_address", "var_1", "var_2", "var_3")
    list_display = ("__str__", "email", "to_address", "draft")

    # email = ForeignKey(EmailMessageTemplate, on_delete=models.CASCADE)
    # send_times = models.PositiveSmallIntegerField(default=0, editable=False)
    # sent_on = models.DateTimeField(null=True, blank=True, editable=False)
    # to_address = models.EmailField(max_length=128)
    # var_1 = models.CharField(max_length=64, null=True, blank=True)
    # var_2 = models.CharField(max_length=64, null=True, blank=True)
    # var_3 = models.CharField(max_length=64, null=True, blank=True)
    # draft = models.BooleanField(default=False)


@admin.register(Sender)
class SenderAdmin(admin.ModelAdmin):
    search_fields = ("name", "address")
    list_display = ("__str__", "name", "address")


@admin.register(EmailMessageTemplate)
class EmailMessageTemplateAdmin(admin.ModelAdmin):
    search_fields = ("body", "subject")
    autocomplete_fields = ("sender",)
    inlines = (AttachmentInline, RecipientInline)
    actions = ("send_emails",)
    list_display = ("subject", "body", "sender", "reply_to", "cc")
    list_editable = ("sender",)
    list_filter = ("is_periodic", "sender")

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


@admin.register(PostalMessage)
class PostalMessageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "mail_from", "mail_to", "direction", "url")
    list_filter = ("status", "tag", "spam_status", "direction")
    readonly_fields = ["url"] + [field.name for field in PostalMessage._meta.fields]
