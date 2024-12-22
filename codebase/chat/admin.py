from django.contrib import admin

from .models import Chat, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("name", "site", "join_full_url")
    readonly_fields = ("name", "site")
    list_filter = ("site",)

    def has_add_permission(self, request):
        return False


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "user", "chat", "body", "deleted")
    list_filter = ("created_at", "user", "deleted")
    list_display = ("__str__", "user", "deleted", "chat")

    def has_add_permission(self, request):
        return False
