from django.contrib import admin, messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from one.admin import OneModelAdmin

from .models import (
    LinkedinAuth,
    LinkedinChannel,
    LinkedinGroupChannel,
    MastodonChannel,
    PostedSocialMediaPost,
    SocialMediaPost,
    TelegramChannel,
    TwitterChannel,
)
from .tasks import task_post_on_social_media
from .utils import get_linkedin_auth_url


@admin.register(SocialMediaPost)
class SocialMediaPostAdmin(OneModelAdmin):
    list_display = ("title", "shared_at", "language", "is_draft")
    list_filter = ("is_draft", "language", "shared_at")
    actions = ("post", "reset_shared", "set_draft", "unset_draft")
    readonly_fields = (
        "shared_at",
        "shared_in_linkedin",
        "shared_in_linkedin_groups",
        "shared_in_twitter",
        "shared_in_mastodon",
        "shared_in_telegram",
    )

    @admin.action(description="⬆️ Publish post")
    def post(modeladmin, request, queryset):
        filtered_qs = queryset.filter(shared_at__isnull=True, is_draft=False)
        if filtered_qs.count() == 1:
            task_post_on_social_media(filtered_qs.first())
        else:
            messages.error(request, "Choose only one object that hasn't been shared.")

    @admin.action(description="🔄 Reset shared")
    def reset_shared(modeladmin, request, queryset):
        queryset.update(
            shared_at=None,
            shared_in_linkedin=False,
            shared_in_linkedin_groups=False,
            shared_in_twitter=False,
            shared_in_mastodon=False,
            shared_in_telegram=False,
        )

    @admin.action(description="📝 Set draft")
    def set_draft(modeladmin, request, queryset):
        queryset.update(is_draft=True)

    @admin.action(description="✅ Unset draft")
    def unset_draft(modeladmin, request, queryset):
        queryset.update(is_draft=False)


@admin.register(LinkedinAuth)
class LinkedinAuthAdmin(OneModelAdmin):
    list_display = ("id", "state", "expires_at", "refresh_token_expires_at")
    list_filter = ("expires_at", "refresh_token_expires_at")
    readonly_fields = (
        "state",
        "code",
        "expires_at",
        "refresh_token_expires_at",
        "scope",
    )
    actions = ("request_code",)

    @admin.action(description="🔑 Request code")
    def request_code(modeladmin, request, queryset):
        if queryset.count() > 1:
            messages.error(
                request,
                _("Not possible to request for multiple channels at the same time."),
            )
            return
        obj = queryset.first()
        url = get_linkedin_auth_url(state=obj.state)
        return redirect(url)


@admin.register(LinkedinChannel)
class LinkedinChannelAdmin(OneModelAdmin):
    list_display = ("name", "author_type", "auth")


@admin.register(LinkedinGroupChannel)
class LinkedinGroupChannelAdmin(OneModelAdmin):
    list_display = ("name", "is_active", "is_private", "languages", "url")
    list_filter = ("is_active", "is_private", "languages")


@admin.register(MastodonChannel)
class MastodonChannelAdmin(OneModelAdmin):
    pass


@admin.register(TelegramChannel)
class TelegramChannelAdmin(OneModelAdmin):
    list_display = ("name", "is_active", "languages", "url")


@admin.register(TwitterChannel)
class TwitterChannelAdmin(OneModelAdmin):
    list_display = ("name", "languages", "topics")


@admin.register(PostedSocialMediaPost)
class PostedSocialMediaPostAdmin(OneModelAdmin):
    list_display = ("post", "content_object", "content_type")
    list_filter = ("content_type", "created_at")
    readonly_fields = [f.name for f in PostedSocialMediaPost._meta.fields]
