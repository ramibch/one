from django.contrib import admin

from .models import EmailTemplate, PastRecipient, Recipient
from .tasks import send_email_templates


@admin.action(description="📧 Send Emails")
def send_emails(modeladmin, request, queryset):
    if queryset.count() > 0:
        ids = tuple(queryset.values_list("id", flat=True))
        send_email_templates(ids)


@admin.action(description="🔄 Recrete recipients")
def recrete_recipients(modeladmin, request, queryset):
    recipients = (
        Recipient(
            email_template=obj.email_template,
            address=obj.address,
            draft=True,
            var1=obj.var1,
            var2=obj.var2,
            var3=obj.var3,
        )
        for obj in queryset
    )
    Recipient.objects.bulk_create(recipients)


class RecipientInline(admin.TabularInline):
    model = Recipient
    extra = 5


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    actions = (send_emails,)
    search_fields = ("body", "subject")
    inlines = (RecipientInline,)


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("__str__", "email_template", "var1", "var2", "var3", "draft")
    list_filter = ("draft", "email_sent", "email_template", "email_sent_on")

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(PastRecipient)
class PastRecipientAdmin(admin.ModelAdmin):
    actions = (recrete_recipients,)
    list_display = ("__str__", "email_template", "email_sent_on")
    list_filter = ("email_template", "email_sent_on")
    readonly_fields = (
        "email_template",
        "subject",
        "body",
        "address",
        "var1",
        "var2",
        "var3",
    )

    def has_add_permission(self, request, obj=None):
        return False
