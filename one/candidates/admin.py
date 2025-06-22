from django.contrib import admin

from one.admin import (
    GISStackedInline,
    OneModelAdmin,
    OneTranslatableModelAdmin,
    OneTranslationStackedInline,
)

from .models import (
    Candidate,
    CandidateJobAlert,
    CandidateSkill,
    JobApplication,
    TexCv,
)
from .tasks import task_render_application_files, task_render_cvs


class AlertInline(GISStackedInline):
    model = CandidateJobAlert
    extra = 1


class SkillInline(OneTranslationStackedInline):
    model = CandidateSkill
    extra = 1


@admin.register(Candidate)
class CandiateProfileAdmin(OneTranslatableModelAdmin):
    list_display = ("id", "full_name", "job_title", "email", "phone")
    inlines = [AlertInline, SkillInline]


@admin.register(CandidateSkill)
class CandidateSkillAdmin(OneTranslatableModelAdmin):
    list_display = ("name", "level", "order")


@admin.register(TexCv)
class TexCvAdmin(OneModelAdmin):
    actions = ["render_cvs"]

    @admin.action(description="▶️ Render CVs")
    def render_cvs(modeladmin, request, queryset):
        task_render_cvs(queryset)


@admin.register(JobApplication)
class JobApplicationAdmin(OneModelAdmin):
    readonly_fields = ("coverletter_text", "dossier_text")
    actions = ["render_coverletters", "render_dossiers"]

    @admin.action(description="▶️ Render Coverletters")
    def render_coverletters(modeladmin, request, queryset):
        task_render_application_files(queryset, coverletters=True)

    @admin.action(description="▶️ Render Dossiers")
    def render_dossiers(modeladmin, request, queryset):
        task_render_application_files(queryset, dossiers=True)
