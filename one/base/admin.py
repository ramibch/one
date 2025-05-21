from django.contrib import admin
from django.contrib.sessions.models import Session
from django.db.migrations.recorder import MigrationRecorder

from one.emails.models import ReplyMessage

from .models import Animation, ContactMessage, SearchTerm


@admin.register(Animation)
class AnimationAdmin(admin.ModelAdmin):
    list_display = ("animation_type", "name", "repeat", "speed", "delay")


@admin.register(MigrationRecorder.Migration)
class MigrationRecorderAdmin(admin.ModelAdmin):
    list_display = ("name", "app", "applied")
    list_filter = ("app", "applied")


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("session_key", "expire_date")
    list_filter = ("expire_date",)
    readonly_fields = ("session_key", "session_data", "expire_date")


@admin.register(SearchTerm)
class SearchTermAdmin(admin.ModelAdmin):
    list_display = ("query", "site", "client", "created_at")
    readonly_fields = ("query", "site", "client", "created_at")
    list_filter = ("site", "created_at")

    def has_add_permission(self, request):
        return False


class ReplyMessageInline(admin.TabularInline):
    model = ReplyMessage
    extra = 1
    max_num = 1
    readonly_fields = ("replied", "replied_on")
    exclude = ("postal_message",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "message", "client", "client__is_blocked")
    list_filter = ("client__is_blocked", "site", "created_at")
    readonly_fields = tuple(field.name for field in ContactMessage._meta.fields)
    inlines = [ReplyMessageInline]
