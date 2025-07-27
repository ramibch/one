from django.contrib import admin

from one.admin import OneModelAdmin

from .models import LinkedinChannel


@admin.register(LinkedinChannel)
class LinkedinChannelAdmin(OneModelAdmin):
    list_display = ("name", "author_type")

    @admin.action(description="🔑 Request code")
    def request_code(modeladmin, request, queryset):
        pass
