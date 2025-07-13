from django.contrib import admin

from .models import User
from .tasks import task_ask_users_to_verify_email


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "country_code", "date_joined")
    list_filter = (
        "asked_to_verify_email",
        "when_asked_to_verify",
        "language",
        "country_code",
    )
    actions = ["ask_to_verify_email"]

    @admin.action(description="📧 Ask to verify Email")
    def ask_to_verify_email(modeladmin, request, queryset):
        task_ask_users_to_verify_email(queryset)
