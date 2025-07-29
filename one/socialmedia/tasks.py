from datetime import timedelta

from django.utils import timezone
from huey import crontab
from huey.contrib import djhuey as huey

from one.bot import Bot

from .models import (
    LinkedinAuth,
    LinkedinChannel,
    LinkedinGroupChannel,
    MastodonChannel,
    SocialMediaPost,
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

    post.shared_at = timezone.now()
    post.save()

    Channels = (LinkedinChannel, LinkedinGroupChannel, TwitterChannel, MastodonChannel)
    for Channel in Channels:
        channels = Channel.objects.filter(
            language=post.language,
            topics__overlap=post.topics,
            is_active=True,
        ).distinct()

        for ch in channels:
            try:
                ch.publish_post(post)
                Bot.to_admin(f"Posted '{post.title}' on {ch.name} ")
            except Exception as e:
                msg = f"Unable to post {post.title} in {ch._meta.model_name}: {e}"
                Bot.to_admin(msg)


"""
# Twitter

In [1]: from django_tweets.clients import get_v2_client

In [2]: xclient = get_v2_client()

In [3]: r = xclient.create_tweet(text="This is just a test using the X API")

In [4]: r
Out[4]: Response(
            data={
                'id': '1949744247101419939',
                'edit_history_tweet_ids': ['1949744247101419939'],
                'text': 'This is just a test using the X API'
            },
            includes={},
            errors=[],
            meta={},
)

In [5]: r.data
Out[5]:
{'id': '1949744247101419939',
 'edit_history_tweet_ids': ['1949744247101419939'],
 'text': 'This is just a test using the X API'}

In [6]: r.data["id"]
Out[6]: '1949744247101419939'

In [7]: type(r)
Out[7]: tweepy.client.Response

In [8]: r.data
Out[8]:
{'id': '1949744247101419939',
 'edit_history_tweet_ids': ['1949744247101419939'],
 'text': 'This is just a test using the X API'}


# use v1 to upload media
    def upload(self):
        # use tempfile to upload the file to the Twitter API.
        # Why tempfile? because not allways media files are not stored locally
        with tempfile.NamedTemporaryFile(suffix="." + self.file_extension) as f:
            f.write(self.file.read())
            f.seek(0)  # https://github.com/tweepy/tweepy/issues/1667
            response = get_v1dot1_api().chunked_upload(f.name)
        # save values into the db
        self.media_id_string = response.media_id_string
        self.response = str(response)
        self.expires_at = timezone.now() + timezone.timedelta(
            seconds=response.expires_after_secs
        )
        if self.delete_after_upload:
            self.file.delete()
        self.save()
        return self


"""
