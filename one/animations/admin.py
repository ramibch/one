from django.contrib import admin

from .models import Animation


@admin.register(Animation)
class AnimationAdmin(admin.ModelAdmin):
    list_display = ("animation_type", "name", "repeat", "speed", "delay")
