from datetime import timedelta

from django.utils import timezone
from huey import crontab
from huey.contrib import djhuey as huey

from one.bot import Bot

from .models import (
    AbstractChannel,
    LinkedinAuth,
    SocialMediaPost,
)
from .utils import refresh_linkedin_access


@huey.db_periodic_task(crontab(hour="4", minute="12"))
def task_check_linkedin_auth_objects():
    now = timezone.now()
    yesterday = now - timedelta(days=1)

    auths = LinkedinAuth.objects.filter(
        expires_at__gte=yesterday,
        refresh_token_expires_at__lt=now,
        code__isnull=False,
    )

    for auth in auths:
        access_data = refresh_linkedin_access(auth.refresh_token)
        auth.update_values(access_data)

    if LinkedinAuth.objects.filter(refresh_token_expires_at__lte=now).exists():
        Bot.to_admin("⚠️ There are expired LinkedinAuth objects!")


@huey.db_periodic_task(crontab(hour="8", minute="45"))
def task_post_on_social_media(post: SocialMediaPost | None = None):
    if post is None:
        post = SocialMediaPost.objects.filter(
            shared_at__isnull=True,
            is_draft=False,
        ).first()

    if post is None:
        return

    post.shared_at = timezone.now()
    post.save()

    for Channel in AbstractChannel.__subclasses__():
        channels = Channel.objects.filter(
            languages__overlap=[post.language],
            topics__overlap=post.topics,
            is_active=True,
        ).distinct()

        for ch in channels:
            try:
                ch.dispatch_post(post)
                Bot.to_admin(f"Posted '{post.title}' on {ch.name} ")
            except Exception as e:
                msg = f"Unable to post {post.title} in {ch._meta.model_name}: {e}"
                Bot.to_admin(msg)
