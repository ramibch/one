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
    task_create_texcvs,
    task_recommend_jobs,
    task_render_coverletters,
    task_render_cvs,
    task_render_dossiers,
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
    actions = ("create_and_render_cvs", "recommend_jobs")

    @admin.action(description="▶️ Create and render CVs")
    def create_and_render_cvs(modeladmin, request, queryset):
        task_create_texcvs(queryset)
        ids = [c.id for c in queryset]
        task_render_cvs(TexCv.objects.filter(candidate__id__in=ids))

    @admin.action(description="💼 Recommend jobs")
    def recommend_jobs(modeladmin, request, queryset):
        task_recommend_jobs(queryset)


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
    list_display = ("__str__", "template", "cv_image", "cv_pdf")
    list_filter = ("template",)
    actions = ("render_cvs",)

    @admin.action(description="▶️ Render CVs")
    def render_cvs(modeladmin, request, queryset):
        task_render_cvs(queryset)


@admin.register(JobApplication)
class JobApplicationAdmin(OneModelAdmin):
    list_display = ("job", "candidate", "language", "dossier")
    readonly_fields = ("coverletter_text", "dossier_text")
    actions = ("render_coverletters", "render_dossiers")
    list_filter = ("language",)

    @admin.action(description="▶️ Render Coverletters")
    def render_coverletters(modeladmin, request, queryset):
        task_render_coverletters(queryset)

    @admin.action(description="▶️ Render Dossiers")
    def render_dossiers(modeladmin, request, queryset):
        task_render_dossiers(queryset)
