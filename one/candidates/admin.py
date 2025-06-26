from django.contrib import admin

from one.admin import (
    GISStackedInline,
    OneModelAdmin,
    OneTranslatableModelAdmin,
    OneTranslationStackedInline,
)

from .models import (
    Candidate,
    CandidateEducation,
    CandidateExperience,
    CandidateJobAlert,
    CandidateSkill,
    JobApplication,
    TexCv,
)
from .tasks import (
    task_create_texcvs_and_render,
    task_render_application_files,
    task_render_cvs,
)


class AlertInline(GISStackedInline):
    model = CandidateJobAlert
    extra = 1


class SkillInline(OneTranslationStackedInline):
    model = CandidateSkill
    extra = 1


class EducationInline(OneTranslationStackedInline):
    model = CandidateEducation
    extra = 1


class ExperienceInline(OneTranslationStackedInline):
    model = CandidateExperience
    extra = 1


@admin.register(Candidate)
class CandiateAdmin(OneTranslatableModelAdmin):
    list_display = ("id", "full_name", "job_title", "email", "phone")
    inlines = [SkillInline, EducationInline, ExperienceInline, AlertInline]
    actions = ["render_cvs"]

    @admin.action(description="▶️ Render CVs")
    def render_cvs(modeladmin, request, queryset):
        task_create_texcvs_and_render(queryset)


@admin.register(CandidateSkill)
class SkillAdmin(OneTranslatableModelAdmin):
    list_display = ("name", "level", "order")


@admin.register(CandidateEducation)
class EducationAdmin(OneTranslatableModelAdmin):
    list_display = ("title", "institution", "start_date", "end_date")


@admin.register(CandidateExperience)
class ExperienceAdmin(OneTranslatableModelAdmin):
    list_display = ("job_title", "company_name", "start_date", "end_date")


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
