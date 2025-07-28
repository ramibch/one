from django.contrib import admin, messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from one.admin import OneModelAdmin

from .models import (
    LinkedinAuth,
    LinkedinChannel,
    MastodonChannel,
    SocialMediaPost,
    TwitterChannel,
)
from .utils import get_linkedin_auth_url


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


@admin.register(TwitterChannel)
class TwitterChannelAdmin(OneModelAdmin):
    list_display = ("name",)


@admin.register(SocialMediaPost)
class SocialMediaPostAdmin(OneModelAdmin):
    pass


@admin.register(MastodonChannel)
class MastodonChannelAdmin(OneModelAdmin):
    pass
