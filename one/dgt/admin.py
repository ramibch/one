from django.contrib import admin

from .models import DgtQuestion, DgtTest, SessionDgtQuestion, SessionDgtTest


class DgtQuestionInline(admin.TabularInline):
    model = DgtQuestion
    extra = 0
    readonly_fields = (
        "title",
        "option_a",
        "option_b",
        "option_c",
        "correct_option",
        "explanation",
        "img_alt",
        "img_url",
    )


@admin.register(DgtTest)
class DgtTestAdmin(admin.ModelAdmin):
    list_display = ("__str__", "source_url")
    inlines = (DgtQuestionInline,)


class SessionDgtQuestionInline(admin.TabularInline):
    model = SessionDgtQuestion
    extra = 0
    readonly_fields = ("created_on", "question", "selected_option", "is_correct")
    exclude = ("session", "test")


@admin.register(SessionDgtTest)
class SessionDgtTestAdmin(admin.ModelAdmin):
    list_display = ("__str__", "test", "created_on")
    list_filter = ("created_on", "test")
    inlines = (SessionDgtQuestionInline,)
    readonly_fields = ("created_on", "test", "session")
