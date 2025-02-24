from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "possible_spam", "country_code", "date_joined")
    list_filter = ("possible_spam", "asked_to_verify_email", "language", "country_code")
