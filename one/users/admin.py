from django.contrib import admin
from django.contrib.auth.models import Permission

from one.admin import OneModelAdmin

from .models import User
from .tasks import task_ask_users_to_verify_email


@admin.register(User)
class UserAdmin(OneModelAdmin):
    list_display = ("username", "email", "country_code", "date_joined")
    list_filter = (
        "asked_to_verify_email",
        "when_asked_to_verify",
        "language",
        "country_code",
    )
    list_select_related = ["content_type", "sites", "groups", "user_permissions"]
    actions = ["ask_to_verify_email"]

    @admin.action(description="📧 Ask to verify Email")
    def ask_to_verify_email(modeladmin, request, queryset):
        task_ask_users_to_verify_email(queryset)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "user_permissions":
            kwargs["queryset"] = Permission.objects.all().select_related("content_type")
        return super().formfield_for_manytomany(db_field, request, **kwargs)
