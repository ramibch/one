from django.conf import settings
from django.contrib import admin

from one.admin import GISStackedInline, OneModelAdmin, OneTranslatableModelAdmin

from .models import CandidateJobAlert, CandidateProfile, JobApplication, TexCv
from .tasks import task_render_coverletters, task_render_cvs, task_render_dossiers


class AlertInline(GISStackedInline):
    model = CandidateJobAlert
    extra = 0


@admin.register(CandidateProfile)
class CandiateProfileAdmin(OneTranslatableModelAdmin):
    list_display = ("id", "full_name", "job_title", "email", "phone")
    inlines = [AlertInline]


@admin.register(TexCv)
class TexCvAdmin(OneModelAdmin):
    actions = ["render_cvs"]

    @admin.action(description="▶️ Render CVs")
    def render_cvs(modeladmin, request, queryset):
        if settings.ENV == settings.PROD:
            task_render_cvs(queryset)
        if settings.ENV == settings.DEV:
            for cv_obj in queryset:
                cv_obj.render_cv()


@admin.register(JobApplication)
class JobApplicationAdmin(OneModelAdmin):
    readonly_fields = ("coverletter_text", "dossier_text")
    actions = ["render_coverletters", "render_dossiers"]

    @admin.action(description="▶️ Render Coverletters")
    def render_coverletters(modeladmin, request, queryset):
        if settings.ENV == settings.PROD:
            task_render_coverletters(queryset)
        if settings.ENV == settings.DEV:
            for cv_obj in queryset:
                cv_obj.render_coverletter()

    @admin.action(description="▶️ Render Dossiers")
    def render_dossiers(modeladmin, request, queryset):
        if settings.ENV == settings.PROD:
            task_render_dossiers(queryset)
        if settings.ENV == settings.DEV:
            for cv_obj in queryset:
                cv_obj.render_dossier()
