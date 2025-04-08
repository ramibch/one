from django.contrib import admin
from django.contrib.sessions.models import Session
from django.db.migrations.recorder import MigrationRecorder

from .models import Animation, SearchTerm, Topic
from .utils.admin import TranslatableModelAdmin


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


@admin.register(Topic)
class TopicAdmin(TranslatableModelAdmin):
    list_display = ("name", "slug", "language", "is_public")
    list_filter = ("language", "is_public")


@admin.register(SearchTerm)
class SearchTermAdmin(admin.ModelAdmin):
    list_display = ("query", "site", "client", "created_on")
    readonly_fields = ("query", "site", "client", "created_on")
    list_filter = ("site", "created_on")

    def has_add_permission(self, request):
        return False
