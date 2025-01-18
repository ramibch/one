import os

from huey import crontab
from huey.contrib import djhuey as huey

from one.base.utils.telegram import Bot

from .models import EmailMessageTemplate


@huey.periodic_task(crontab(minute="*"))
def task_send_email_templates(queryset=None):
    """
    Send emails for recipients from Email Templates.
    """

    if queryset is None:
        queryset = EmailMessageTemplate.objects.filter(is_periodic=True)

    for email in queryset:
        count = 0
        log = f"📧 {email.subject}\n\n"
        for recipient in email.recipient_set.filter(draft=False):
            if not recipient.allow_to_send_email:
                continue
            try:
                recipient.send_email()
                log += f"✅ Sent to {recipient}\n"
                count += 1
            except Exception as e:
                log += f"⚠️  Error with recipient {recipient}: {e}\n"

        if count > 0:
            Bot.to_admin(log)

        # Remove tmp files
        for local_attachment in email.get_local_attachments():
            os.unlink(local_attachment)
