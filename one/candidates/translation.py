from modeltranslation.translator import TranslationOptions, register

from .models import (
    CandidateCertificate,
    CandidateEducation,
    CandidateExperience,
    CandidateProfile,
    CandidateProject,
    CandidateSkill,
)


@register(CandidateProfile)
class CandidateProfileOptions(TranslationOptions):
    fields = (
        "job_title",
        "location",
        "about",
        "coverletter_body",
        "about_label",
        "experience_label",
        "education_label",
        "skill_label",
        "certificate_label",
        "language_label",
        "project_label",
    )


@register(CandidateExperience)
class CandidateExperienceOptions(TranslationOptions):
    fields = ("job_title", "from_to", "description")


@register(CandidateEducation)
class CandidateEducationOptions(TranslationOptions):
    fields = ("title", "from_to", "description")


@register(CandidateSkill)
class CandidateSkillOptions(TranslationOptions):
    fields = ("name",)


@register(CandidateCertificate)
class CandidateCertificateOptions(TranslationOptions):
    fields = ("name",)


@register(CandidateProject)
class CandidateProjectOptions(TranslationOptions):
    fields = ("title", "from_to", "description")
