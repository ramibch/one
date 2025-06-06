from django.conf import settings
from django.contrib import admin

from one.admin import GISStackedInline, OneModelAdmin, OneTranslatableModelAdmin

from .models import CandidateJobAlert, CandidateProfile, JobApplication, TexCv
from .tasks import task_render_coverletters, task_render_cvs


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
        match settings.ENV:
            case settings.PROD:
                task_render_cvs(queryset)
            case settings.DEV:
                for cv_obj in queryset:
                    cv_obj.render_cv()


@admin.register(JobApplication)
class JobApplicationAdmin(OneModelAdmin):
    actions = ["render_coverletters"]

    @admin.action(description="▶️ Render Coverletters")
    def render_coverletters(modeladmin, request, queryset):
        match settings.ENV:
            case settings.PROD:
                task_render_coverletters(queryset)
            case settings.DEV:
                for job_app in queryset:
                    job_app.render_coverletter()
