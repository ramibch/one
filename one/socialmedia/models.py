import json
import secrets
from datetime import timedelta

import requests
import tweepy
from auto_prefetch import ForeignKey
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from mastodon import Mastodon

from one.bot import Bot
from one.choices import Topics
from one.db import ChoiceArrayField, OneModel
from one.quiz.models import Question as EnglishQuestion
from one.tmp import TmpFile

from .linkedin import LinkedinClient


class SocialMediaPost(OneModel):
    title = models.CharField(max_length=256)
    text = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to="socialmedia/")
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

    # linkedin channels
    share_in_linkedin = models.BooleanField(default=True)
    shared_in_linkedin = models.BooleanField(default=False, editable=False)

    # linkedin group channels
    share_in_linkedin_groups = models.BooleanField(default=True)
    shared_in_linkedin_groups = models.BooleanField(default=False, editable=False)

    # twitter channels
    share_in_twitter = models.BooleanField(default=True)
    shared_in_twitter = models.BooleanField(default=False, editable=False)

    # mastodon channels
    share_in_mastodon = models.BooleanField(default=True)
    shared_in_mastodon = models.BooleanField(default=False, editable=False)

    # telegram channels
    share_in_telegram = models.BooleanField(default=True)
    shared_in_telegram = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return self.text[:100]

    @property
    def local_image_path(self) -> str | None:
        if self.image.name == "":
            return
        return str(TmpFile(self.image).path)


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
    name = models.CharField(max_length=128)
    post_jobs = models.BooleanField(default=False)
    post_english = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    topics = ChoiceArrayField(
        models.CharField(max_length=16, choices=Topics),
        default=list,
        blank=True,
    )
    languages = ChoiceArrayField(
        models.CharField(max_length=8, choices=settings.LANGUAGES),
        default=list,
        blank=True,
    )

    def __str__(self) -> str:
        return self.name

    class Meta(OneModel.Meta):
        abstract = True

    def dispatch_post(self, post: SocialMediaPost):
        if post.shared_at or post.is_draft:
            Bot.to_admin(f"Post '{post.text}' is draft or is already shared.")
            return
        self.handle_post_publish(post)

    def handle_post_publish(self, post: SocialMediaPost):
        raise NotImplementedError("Subclasses must implement `handle_post_publish`")


def build_linkedin_content(client: LinkedinClient, post: SocialMediaPost):
    """
    One image:
        {"media": {"title": images[0].title, "id": images[0].urn}}

    Multiple images:
        multi = [{"id": i.urn, "altText": i.title} for i in images]
        return {"multiImage": {"images": multi}}
    """

    if post.image.name == "":
        return None

    response, urn = client.upload_image(post.image.read())
    response.raise_for_status()
    return {"media": {"title": post.title, "id": urn}}


class PostedSocialMediaContent(OneModel):
    # channel
    channel_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="channel_posted_contents",
        limit_choices_to={
            "model__in": [
                "linkedinchannel",
                "linkedingroupchannel",
                "twitterchannel",
                "mastodonchannel",
                "telegramchannel",
            ]
        },
    )
    channel_id = models.PositiveBigIntegerField()
    channel_object = GenericForeignKey("channel_type", "channel_id")
    # posted object
    post_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="post_posted_contents",
        limit_choices_to={
            "model__in": ["socialmediapost", "question"],
            "app_label__in": ["quiz", "socialmedia"],
        },
    )
    post_id = models.PositiveBigIntegerField()
    post_object = GenericForeignKey("post_type", "post_id")

    # response
    response_json = models.JSONField()
    response_headers = models.JSONField(null=True)
    respose_status = models.PositiveSmallIntegerField(null=True)

    def __str__(self) -> str:
        return f"{self.post_object} - {self.channel_object}"


class LinkedinChannel(AbstractChannel):
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

    def save_posted_content(
        self,
        post_object: SocialMediaPost | EnglishQuestion,
        response: requests.Response,
    ):
        posted = PostedSocialMediaContent(
            channel_type=ContentType.objects.get_for_model(LinkedinChannel),
            channel_id=self.pk,
            channel_object=self,
            post_type=ContentType.objects.get_for_model(type(post_object)),
            post_id=post_object.pk,
            post_object=post_object,
            response_json=json.loads(response.text),
            response_headers=dict(response.headers),
            respose_status=response.status_code,
        )
        posted.save()

    def handle_post_publish(self, post: SocialMediaPost):
        if not post.share_in_linkedin or post.shared_in_linkedin:
            msg = f"Not possible to share '{post}' in Linkedin Channel '{self.name}'"
            Bot.to_admin(msg)
            return
        li_content = build_linkedin_content(self.client, post)
        response = self.client.share_post(comment=post.text, content=li_content)
        self.save_posted_content(post, response)

    def post_english_question(self, question: EnglishQuestion):
        text = question.get_question_promotion_text(add_link=False)
        response = self.client.share_post(comment=text)
        self.save_posted_content(question, response)


class LinkedinGroupChannel(AbstractChannel):
    channel = ForeignKey(LinkedinChannel, on_delete=models.CASCADE)
    group_id = models.CharField(max_length=64, unique=True)
    is_private = models.BooleanField(default=True)

    @cached_property
    def url(self):
        return f"https://www.linkedin.com/groups/{self.group_id}"

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

    def save_posted_content(
        self,
        post_object: SocialMediaPost | EnglishQuestion,
        response: requests.Response,
    ):
        posted = PostedSocialMediaContent(
            channel_type=ContentType.objects.get_for_model(LinkedinGroupChannel),
            channel_id=self.pk,
            channel_object=self,
            post_type=ContentType.objects.get_for_model(type(post_object)),
            post_id=post_object.pk,
            post_object=post_object,
            response_json=json.loads(response.text),
            response_headers=dict(response.headers),
            respose_status=response.status_code,
        )
        posted.save()

    def handle_post_publish(self, post: SocialMediaPost):
        if not post.share_in_linkedin_groups or post.shared_in_linkedin_groups:
            msg = f"Not possible to share '{post}' in Linkedin Group '{self.name}'"
            Bot.to_admin(msg)
            return

        response = self.client.share_post(
            comment=post.text,
            visibility=self.li_visibility,
            content=build_linkedin_content(self.client, post),
            container=self.li_container,
        )
        self.save_posted_content(post, response)

    def post_english_question(self, question: EnglishQuestion):
        text = question.get_question_promotion_text(add_link=False)
        response = self.client.share_post(comment=text)
        self.save_posted_content(question, response)


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
            return_type=requests.Response,  # type: ignore
        )

    @property
    def client_v1_1(self) -> tweepy.API:
        auth = tweepy.OAuth1UserHandler(self.api_key, self.api_key_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        return tweepy.API(auth, wait_on_rate_limit=True)

    def save_posted_content(
        self,
        post_object: SocialMediaPost | EnglishQuestion,
        response: requests.Response,
    ):
        posted = PostedSocialMediaContent(
            channel_type=ContentType.objects.get_for_model(TwitterChannel),
            channel_id=self.pk,
            channel_object=self,
            post_type=ContentType.objects.get_for_model(type(post_object)),
            post_id=post_object.pk,
            post_object=post_object,
            response_json=json.loads(response.text),
            response_headers=dict(response.headers),
            respose_status=response.status_code,
        )
        posted.save()

    def handle_post_publish(self, post: SocialMediaPost):
        if not post.share_in_twitter or post.shared_in_twitter:
            msg = f"Not possible to share '{post}' in Twitter Channel '{self.name}'"
            Bot.to_admin(msg)
            return
        params = {"text": post.text}
        if post.image.name != "":
            media_response = self.client_v1_1.chunked_upload(post.local_image_path)
            params["media_ids"] = [media_response.media_id_string]
        response = self.client_v2.create_tweet(**params)

        self.save_posted_content(post, response)  # type: ignore

    def post_english_question(self, question: EnglishQuestion):
        text = question.get_question_promotion_text(add_link=False)
        response = self.client_v2.create_tweet(text=text)
        self.save_posted_content(question, response)  # type: ignore


class MastodonChannel(AbstractChannel):
    access_token = models.CharField(max_length=256)
    api_base_url = models.URLField(max_length=256)

    @property
    def client(self) -> Mastodon:
        return Mastodon(access_token=self.access_token, api_base_url=self.api_base_url)

    def handle_post_publish(self, post: SocialMediaPost):
        if not post.share_in_mastodon or post.shared_in_mastodon:
            msg = f"Not possible to share '{post}' in Mastodon Channel '{self.name}'"
            Bot.to_admin(msg)
            return
        parameters = {"status": post.text}
        if post.image.name != "":
            media_response = self.client.media_post(post.local_image_path)  # type: ignore
            parameters["media_ids"] = [media_response.id]
        self.client.status_post(**parameters)


class TelegramChannel(AbstractChannel):
    group_id = models.CharField(max_length=64, unique=True)

    @cached_property
    def url(self):
        return f"https://t.me/{self.group_id}"

    def handle_post_publish(self, post: SocialMediaPost):
        if not post.share_in_telegram or post.shared_in_telegram:
            msg = f"Not possible to share '{post}' in Telegram Channel '{self.name}'"
            Bot.to_admin(msg)
            return
        Bot.to_group(
            group_id=self.group_id,
            text=post.text,
            file_url=post.image.url if post.image.name != "" else None,
        )
