import random
from datetime import timedelta

from django.utils import timezone
from huey import crontab
from huey.contrib import djhuey as huey

from one.bot import Bot
from one.quiz.models import Question

from .models import (
    LinkedinAuth,
    LinkedinChannel,
    LinkedinGroupChannel,
    MastodonChannel,
    SocialMediaPost,
    TelegramChannel,
    TwitterChannel,
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

    filters = {
        "languages__overlap": [post.language],
        "topics__overlap": post.topics,
        "is_active": True,
    }

    def handle_platform(share_flag: bool, shared_attr: str, model_cls):
        if not share_flag or getattr(post, shared_attr):
            return
        for ch in model_cls.objects.filter(**filters).distinct():
            try:
                ch.dispatch_post(post)
            except Exception as e:
                msg = f"Unable to post '{post}' in '{ch}' ({model_cls.__name__}): {e}"
                Bot.to_admin(msg)
        setattr(post, shared_attr, True)

    handle_platform(
        post.share_in_linkedin,
        "shared_in_linkedin",
        LinkedinChannel,
    )
    handle_platform(
        post.share_in_linkedin_groups,
        "shared_in_linkedin_groups",
        LinkedinGroupChannel,
    )
    handle_platform(
        post.share_in_twitter,
        "shared_in_twitter",
        TwitterChannel,
    )
    handle_platform(
        post.share_in_mastodon,
        "shared_in_mastodon",
        MastodonChannel,
    )
    handle_platform(
        post.share_in_telegram,
        "shared_in_telegram",
        TelegramChannel,
    )

    post.shared_at = timezone.now()
    post.save()


@huey.db_periodic_task(crontab(hour="12", minute="00"))
def task_share_random_quiz_question():
    """
    Share english quiz question
    """
    question = random.choice(list(Question.objects.filter(promoted=False)))
    text = question.get_question_promotion_text(add_link=False)
    # text_with_link = question.get_question_promotion_text(add_link=True)

    li_channels = LinkedinChannel.objects.filter(post_english=True, is_active=True)
    x_channels = TwitterChannel.objects.filter(post_english=True, is_active=True)

    for ch in li_channels:
        ch.client.share_post(comment=text)

    for ch in x_channels:
        ch.client_v2.create_tweet(text=text)


@huey.db_periodic_task(crontab(hour="9", minute="15"))
def task_share_random_quiz_question_as_poll():
    """
    Share english quiz question as poll
    """
    question = random.choice(list(Question.objects.filter(type=5)))
    options = question.get_answer_list()
    comment = question.get_poll_explanation_text(add_link=False)
    question = question.full_text

    for channel in LinkedinChannel.objects.filter(post_english=True):
        channel.client.share_poll(question=question, options=options, comment=comment)
