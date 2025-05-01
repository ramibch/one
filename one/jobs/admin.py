from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple

from .models import (
    Application,
    Certificate,
    Company,
    Education,
    Experience,
    HiringReason,
    Job,
    Language,
    Location,
    Position,
    Profile,
    Project,
    Recruiter,
    Skill,
)
from .tasks import (
    render_dossiers_task,
    send_jobapps_per_email_task,
    send_jobapps_per_sms_task,
)

FORMFIELD_OVERRIDE = {
    models.ManyToManyField: {"widget": CheckboxSelectMultiple},
}


class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 1


class EducationInline(admin.TabularInline):
    model = Education
    extra = 1


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


class CertificateInline(admin.TabularInline):
    model = Certificate
    extra = 1


class ProjectInline(admin.TabularInline):
    model = Project
    extra = 1


class LanguageInline(admin.TabularInline):
    model = Language
    extra = 1


class HiringReasonInline(admin.TabularInline):
    model = HiringReason
    extra = 2


@admin.register(Location)
class LocationAmin(admin.ModelAdmin):
    pass


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("__str__", "position_type", "remote")
    list_filter = ("position_type", "remote")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    formfield_overrides = FORMFIELD_OVERRIDE
    actions = ("duplicate_objs", "create_applications")
    search_fields = ("fullname", "email", "phone")
    list_display = ("__str__", "email", "phone", "is_rami")
    list_filter = ("is_rami", "lang", "position", "locations")
    inlines = (
        ExperienceInline,
        EducationInline,
        SkillInline,
        LanguageInline,
        CertificateInline,
        ProjectInline,
    )

    @admin.action(description="📋 Duplicate objects")
    def duplicate_objs(modeladmin, request, queryset):
        for obj in queryset:
            obj.clone_obj(attrs={"job_title": obj.job_title + " (copy)"})

    @admin.action(description="💼 Create applications")
    def create_applications(modeladmin, request, queryset):
        # queryset -> profiles
        applications = []
        for p in queryset:
            jobs = Job.objects.filter(
                position=p.position, location__in=p.locations.all(), lang=p.lang
            ).distinct()
            for job in jobs:
                try:
                    Application.objects.get(profile=p, job=job)
                except Application.DoesNotExist:
                    applications.append(Application(profile=p, job=job, draft=True))
        Application.objects.bulk_create(applications)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    actions = (
        "set_draft",
        "unset_draft",
        "render_dossiers",
        "send_emails",
        "send_smss",
        "full_process",
    )
    autocomplete_fields = ("profile", "job")
    list_display = ("__str__", "profile", "email_sent", "email_sent_on", "dossier")
    readonly_fields = ("candidate_informed", "dossier", "letter", "cv")
    list_filter = (
        "draft",
        "email_sent",
        "job__company__email_allowed",
        "email_sent_on",
        "profile",
    )
    inlines = (HiringReasonInline,)

    @admin.action(description="📝 Set draft")
    def set_draft(modeladmin, request, queryset):
        queryset.update(draft=True)

    @admin.action(description="✅ Set as no draft")
    def unset_draft(modeladmin, request, queryset):
        queryset.update(draft=False)

    @admin.action(description="🧑‍💼 Render dossiers")
    def render_dossiers(modeladmin, request, queryset):
        render_dossiers_task(tuple(queryset.values_list("id", flat=True)))

    @admin.action(description="📧 Send Emails")
    def send_emails(modeladmin, request, queryset):
        send_jobapps_per_email_task(tuple(queryset.values_list("id", flat=True)))

    @admin.action(description="💬 Send SMSs")
    def send_smss(modeladmin, request, queryset):
        send_jobapps_per_sms_task(tuple(queryset.values_list("id", flat=True)))

    @admin.action(description="👉 Full process")
    def full_process(modeladmin, request, queryset):
        modeladmin.unset_draft(request, queryset)
        modeladmin.render_dossiers(request, queryset)
        modeladmin.send_emails(request, queryset)
        modeladmin.send_smss(request, queryset)


@admin.register(Recruiter)
class RecruiterAdmin(admin.ModelAdmin):
    autocomplete_fields = ["company"]
    search_fields = ("name", "company__name", "email", "phone", "remarks")
    list_display = ("name", "company", "email", "phone", "remarks")


class RecruiterInline(admin.TabularInline):
    model = Recruiter
    extra = 1


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    inlines = (RecruiterInline,)
    search_fields = ("name",)
    list_display = ("name", "address", "email_allowed")
    list_filter = ("email_allowed",)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    formfield_overrides = FORMFIELD_OVERRIDE
    autocomplete_fields = ("company", "recruiter")
    search_fields = ("title", "company__name", "recruiter__name", "extern_id")
    list_display = ("__str__", "company", "recruiter", "extern_id", "url")
    list_filter = ("promoted", "lang", "position", "location")
