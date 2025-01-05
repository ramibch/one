from huey.contrib import djhuey as huey

from utils.telegram import report_to_admin

from .models import EmailTemplate


def bulk_send(template_emails):
    reporting = "📧 Sending Emails"
    for template_email in template_emails:
        reporting += "\n\n" + template_email.subject + ":\n"
        recipients = template_email.recipient_set.filter(draft=False, email_sent=False)
        for recipient in recipients:
            try:
                recipient.send_email()
                reporting += f"✅ Sent to {recipient}\n"
            except Exception as e:
                reporting += f"⚠️  Error with recipient {recipient}: {e}\n"

    report_to_admin(reporting)


@huey.task()
def send_email_templates(ids=tuple):
    bulk_send(EmailTemplate.objects.filter(id__in=ids))
