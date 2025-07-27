from datetime import timedelta

from django.utils import timezone
from huey import crontab
from huey.contrib import djhuey as huey

from one.bot import Bot

from .models import LinkedinAuth
from .utils import refresh_linkedin_access


@huey.db_periodic_task(crontab(hour="4", minute="12"))
def task_check_linkedin_auth_objects():
    auths = LinkedinAuth.objects.filter(
        expires_at__gte=timezone.now() - timedelta(days=1),
        refresh_token_expires_at__lt=timezone.now(),
        code__isnull=False,
    )
    for auth in auths:
        access_data = refresh_linkedin_access(auth.refresh_token)
        auth.update_values(access_data)

    if LinkedinAuth.objects.filter(
        refresh_token_expires_at__gt=timezone.now()
    ).exists():
        Bot.to_admin("⚠️ There are expired LinkedinAuth objects!")
