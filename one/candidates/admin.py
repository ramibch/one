from django.contrib import admin

from one.admin import GISStackedInline, OneModelAdmin

from .models import CandidateJobAlert, CandidateProfile


class AlertInline(GISStackedInline):
    model = CandidateJobAlert
    extra = 0


@admin.register(CandidateProfile)
class CandiateProfileAdmin(OneModelAdmin):
    list_display = ("id", "full_name", "job_title", "email", "phone")
    inlines = [AlertInline]
