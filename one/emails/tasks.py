from huey import crontab
from huey.contrib import djhuey as huey

from one.base.utils.telegram import Bot

from .models import (
    PostalMessage,
    PostalReplyMessage,
    TemplateMessage,
    TemplateRecipient,
)


@huey.db_task()
def task_send_email_templates(queryset):
    """
    Send emails for recipients from Email Templates.
    """
    for email in queryset:
        count = 0
        log = f"📧 {email.subject}\n\n"
        for recipient in email.templaterecipient_set.filter(draft=False):
            if not recipient.allow_to_send_email():
                log += f"⏭️ Skip {recipient}\n"
                continue
            try:
                recipient.send_email(fail_silently=False)
                log += f"✅ Sent to {recipient}\n"
                count += 1
            except Exception as e:
                log += f"⚠️  Error with recipient {recipient}: {e}\n"

        if count > 0:
            Bot.to_admin(log)


@huey.db_periodic_task(crontab(minute="*"))
def task_send_periodic_email_templates_and_reply_postal_messages():
    """
    Send emails for recipients from Email Templates.
    """
    emails = TemplateMessage.objects.filter(is_periodic=True)
    if emails.count() > 0:
        task_send_email_templates.schedule((emails,), delay=1)

    replies = PostalReplyMessage.objects.filter(replied=False, draft=False)

    for reply_obj in replies:
        reply_obj.reply(fail_silently=False)


@huey.db_periodic_task(crontab(hour="12", minute="18"))
def task_mark_recipient_as_draft_due_hard_fails():
    fails = list(
        PostalMessage.objects.filter(status__in=["HardFail", "SoftFail"])
        .values_list("mail_to", flat=True)
        .distinct()
    )
    TemplateRecipient.objects.filter(to_address__in=fails).update(draft=True)
