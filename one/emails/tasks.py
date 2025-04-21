from datetime import timedelta

from django.utils import timezone
from huey import crontab
from huey.contrib import djhuey as huey

from one import settings
from one.base.utils.telegram import Bot

from .models import (
    PostalMessage,
    ReplyMessage,
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
def task_send_periodic_email_templates_and_reply_messages():
    """
    Send emails for recipients from Email Templates.
    """
    emails = TemplateMessage.objects.filter(is_periodic=True)
    if emails.count() > 0:
        task_send_email_templates.schedule((emails,), delay=1)

    reply_objs = ReplyMessage.objects.filter(
        replied=False,
        draft=False,
        sender__isnull=False,
    )

    for obj in reply_objs:
        obj.reply(fail_silently=False)


@huey.db_periodic_task(crontab(hour="12", minute="18"))
def task_mark_recipient_as_draft_due_hard_fails():
    fails = list(
        PostalMessage.objects.filter(status__in=["HardFail", "SoftFail"])
        .values_list("mail_to", flat=True)
        .distinct()
    )
    TemplateRecipient.objects.filter(to_address__in=fails).update(draft=True)


@huey.db_periodic_task(crontab(hour="0", minute="43"))
def remove_messages_sent_to_admins():
    PostalMessage.objects.filter(
        received_at__lt=timezone.now() - timedelta(days=2),
        mail_to__in=[a[1] for a in settings.ADMINS],
    ).delete()
