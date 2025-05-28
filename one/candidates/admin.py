from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from .models import CandidateApplicationLocation, CandidateProfile


@admin.register(CandidateProfile)
class CandiateProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "job_title", "email", "phone")


@admin.register(CandidateApplicationLocation)
class CandidateApplicationLocation(GISModelAdmin):
    pass
