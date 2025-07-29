import secrets
from datetime import timedelta

import tweepy
from auto_prefetch import ForeignKey
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from mastodon import Mastodon

from one.bot import Bot
from one.choices import Topics
from one.db import ChoiceArrayField, OneModel

from .linkedin import LinkedinClient


class SocialMediaPost(OneModel):
    title = models.CharField(max_length=256)
    text = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to="socialmedia/")
    image_li_urn = models.CharField(max_length=64, null=True, blank=True)
    shared_at = models.DateTimeField(null=True, blank=True)
    topics = ChoiceArrayField(
        models.CharField(max_length=16, choices=Topics),
        default=list,
        blank=True,
    )
    language = models.CharField(
        max_length=4,
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE,
    )
    is_draft = models.BooleanField(default=True)

    def __str__(self):
        return self.text[:100]


class LinkedinAuthorType(models.TextChoices):
    PERSON = "person", _("Person")
    ORGANIZATION = "organization", _("Organization")


class LinkedinAuth(OneModel):
    state = models.CharField(max_length=128, default=secrets.token_hex)
    code = models.TextField(blank=True, null=True)
    access_token = models.TextField(blank=True, null=True, editable=False)
    expires_at = models.DateTimeField(blank=True, null=True)
    refresh_token = models.TextField(blank=True, null=True, editable=False)
    refresh_token_expires_at = models.DateTimeField(blank=True, null=True)
    scope = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"[{self.pk}] {self.state}"

    def update_values(self, access_data: dict, code: str | None = None):
        """
        access_data = {
                      "access_token": <access_token>,
                      "expires_in": 86400,
                      "refresh_token": <refresh_token>,
                      "refresh_token_expires_in": 439200,
                      "scope":"r_basicprofile"
                      }
        """

        if code:
            self.code = code

        log = [f"🔄 Updating LinkedinAuth ({self.pk})"]

        if "access_token" in access_data:
            self.access_token = access_data["access_token"]
            log.append("✅ access_token received")
        else:
            log.append("⚠️ access_token missing")

        if "refresh_token" in access_data:
            self.refresh_token = access_data["refresh_token"]
            log.append("✅ refresh_token received")
        else:
            log.append("⚠️ refresh_token missing")

        if "expires_in" in access_data:
            self.expires_at = timezone.now() + timedelta(
                seconds=access_data["expires_in"]
            )
            log.append(f"✅ expires_in set to {self.expires_at}")
        else:
            log.append("⚠️ expires_in missing")

        if "refresh_token_expires_in" in access_data:
            self.refresh_token_expires_at = timezone.now() + timedelta(
                seconds=access_data["refresh_token_expires_in"]
            )
            log.append(
                f"✅ refresh_token_expires_in set to {self.refresh_token_expires_at}"
            )
        else:
            log.append("⚠️ refresh_token_expires_in missing")

        if "scope" in access_data:
            self.scope = access_data["scope"]
            log.append("✅ scope set")
        else:
            log.append("⚠️ scope missing")

        self.save()
        Bot.to_admin("\n".join(log))


class AbstractChannel(OneModel):
    name = models.CharField(max_length=64)
    post_jobs = models.BooleanField(default=False)
    post_english = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    topics = ChoiceArrayField(
        models.CharField(max_length=16, choices=Topics),
        default=list,
        blank=True,
    )
    language = models.CharField(
        max_length=4,
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE,
    )

    def __str__(self) -> str:
        return self.name

    class Meta(OneModel.Meta):
        abstract = True

    def publish_post(self, post):
        raise NotImplementedError("Implement this method in the subclass")


class AbstractLinkedinChannel(AbstractChannel):
    client = LinkedinClient(access_token="", author_id="", author_type="")

    class Meta(AbstractChannel.Meta):
        abstract = True

    def build_content(self, post: SocialMediaPost):
        """
        One image:
            {"media": {"title": images[0].title, "id": images[0].urn}}

        Multiple images:
            multi = [{"id": i.urn, "altText": i.title} for i in images]
            return {"multiImage": {"images": multi}}
        """

        if post.image.name == "":
            return None

        if post.image_li_urn is None:
            r, urn = self.client.upload_image(post.image.read())
            post.image_li_urn = urn
            post.save()

        return {"media": {"title": post.title, "id": post.image_li_urn}}


class LinkedinChannel(AbstractLinkedinChannel):
    auth = ForeignKey(LinkedinAuth, on_delete=models.CASCADE)
    author_id = models.CharField(max_length=32)
    author_type = models.CharField(max_length=32, choices=LinkedinAuthorType)

    @property
    def client(self) -> LinkedinClient:
        return LinkedinClient(
            access_token=self.auth.access_token,
            author_type=self.author_type,
            author_id=self.author_id,
        )

    def publish_post(self, post: SocialMediaPost):
        self.client.share_post(
            comment=post.text,
            visibility="PUBLIC",
            feed_distribution="MAIN_FEED",
            reshable_disabled=False,
            content=self.build_content(post),
            container=None,
        )


class LinkedinGroupChannel(AbstractLinkedinChannel):
    channel = ForeignKey(LinkedinChannel, on_delete=models.CASCADE)
    group_id = models.CharField(max_length=64, unique=True)
    is_private = models.BooleanField(default=True)

    @property
    def client(self) -> LinkedinClient:
        return LinkedinClient(
            access_token=self.channel.auth.access_token,
            author_type=self.channel.author_type,
            author_id=self.channel.author_id,
        )

    @property
    def li_visibility(self):
        return "CONTAINER" if self.is_private else "PUBLIC"

    @property
    def li_container(self):
        return "urn:li:group:" + self.group_id

    def publish_post(self, post: SocialMediaPost):
        self.client.share_post(
            comment=post.text,
            visibility=self.li_visibility,
            feed_distribution="MAIN_FEED",
            reshable_disabled=False,
            content=self.build_content(post),
            container=self.li_container,
        )


class TwitterChannel(AbstractChannel):
    bearer_token = models.CharField(max_length=256)
    api_key = models.CharField(max_length=256)
    api_key_secret = models.CharField(max_length=256)
    access_token = models.CharField(max_length=256)
    access_token_secret = models.CharField(max_length=256)

    @property
    def client_v2(self) -> tweepy.Client:
        return tweepy.Client(
            bearer_token=self.bearer_token,
            consumer_key=self.api_key,
            consumer_secret=self.api_key_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret,
        )

    @property
    def client_v1_1(self) -> tweepy.API:
        auth = tweepy.OAuthHandler(self.api_key, self.api_key_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        return tweepy.API(auth, wait_on_rate_limit=True)


class MastodonChannel(AbstractChannel):
    access_token = models.CharField(max_length=256)
    api_base_url = models.URLField(max_length=256)

    @property
    def client(self) -> Mastodon:
        return Mastodon(access_token=self.access_token, api_base_url=self.api_base_url)
