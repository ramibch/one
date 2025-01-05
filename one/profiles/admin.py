from django.contrib import admin

from cvs.models import Cv

from .models import (
    Achievement,
    Education,
    Experience,
    LanguageAbility,
    Profile,
    Project,
    Publication,
    Skill,
)


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 0


class CvInline(admin.TabularInline):
    model = Cv
    extra = 0


class LanguageInline(admin.TabularInline):
    model = LanguageAbility
    extra = 0


class EducationInline(admin.StackedInline):
    model = Education
    extra = 0


class ExperienceInline(admin.StackedInline):
    model = Experience
    extra = 0


class AchievementInline(admin.TabularInline):
    model = Achievement
    extra = 0


class ProjectInline(admin.TabularInline):
    model = Project
    extra = 0


class PublicationInline(admin.TabularInline):
    model = Publication
    extra = 0


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["__str__", "category", "language_code", "created"]
    list_filter = ["category", "public", "language_code", "created"]
    inlines = [
        CvInline,
        SkillInline,
        LanguageInline,
        EducationInline,
        ExperienceInline,
        AchievementInline,
        ProjectInline,
        PublicationInline,
    ]
