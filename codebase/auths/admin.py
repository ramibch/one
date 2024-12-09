from django.contrib import admin

from .models import Etsy


@admin.register(Etsy)
class EtsyAdmin(admin.ModelAdmin):
    readonly_fields = (
        "access_token",
        "refresh_token",
        "expires_at",
        "code_verifier",
        "state",
        "code",
    )
    list_display = ("name", "keystring")
