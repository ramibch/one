from huey import crontab
from huey.contrib import djhuey as huey

from one.base.utils.telegram import Bot

from .models import MessageTemplate


@huey.task()
def task_send_email_templates(queryset):
    """
    Send emails for recipients from Email Templates.
    """
    for email_template in queryset.filter(is_periodic=False):
        log = f"📧 {email_template.subject}\n\n"
        recipients = email_template.recipient_set.filter(draft=False, email_sent=False)
        for recipient in recipients:
            try:
                recipient.send_email()
                log += f"✅ Sent to {recipient}\n"
            except Exception as e:
                log += f"⚠️  Error with recipient {recipient}: {e}\n"
        Bot.to_admin(log)


@huey.periodic_task(crontab(minute="*"))
def task_send_periodic_email_templates():
    """
    Send emails for recipients from Email Templates.
    """
    for email_template in MessageTemplate.objects.filter(is_periodic=True):
        log = f"📧 {email_template.subject}\n\n"
        recipients = email_template.recipient_set.filter(draft=False)
        for recipient in recipients:
            try:
                recipient.send_email()
                log += f"✅ Sent to {recipient}\n"
            except Exception as e:
                log += f"⚠️  Error with recipient {recipient}: {e}\n"
        Bot.to_admin(log)
