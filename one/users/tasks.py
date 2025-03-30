from allauth.account.models import EmailAddress
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone, translation
from django.utils.translation import gettext_lazy as _
from huey import crontab
from huey.contrib import djhuey as huey

from .models import User


@huey.db_periodic_task(crontab(minute="1"))
def task_ask_users_to_verify_email():
    """
    Ask users to verify their corresponding email addresses
    """
    users = User.objects.filter(
        email__in=EmailAddress.objects.filter(verified=False).values_list("email"),
        asked_to_verify_email=False,
        language__isnull=False,
        sites__isnull=False,
    )

    for user in users:
        with translation.override(user.language):
            site = user.sites.last()

            subject = _("Verify your email") + " 🙂"
            body = render_to_string(
                "emails/verify_email.txt",
                context={"site": site, "user": user},
                request=None,
            )
            EmailMessage(
                subject=subject,
                body=body,
                from_email=site.from_email_address,
                to=[user.email],
            ).send(fail_silently=True)

    users.update(asked_to_verify_email=True, when_asked_to_verify=timezone.now())
