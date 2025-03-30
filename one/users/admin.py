from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "country_code", "date_joined")
    list_filter = (
        "asked_to_verify_email",
        "language",
        "country_code",
        "when_asked_to_verify",
    )
