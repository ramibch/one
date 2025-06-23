from modeltranslation.translator import TranslationOptions, register

from .models import (
    Candidate,
    CandidateEducation,
    CandidateExperience,
    CandidateSkill,
)


@register(Candidate)
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
    )


@register(CandidateSkill)
class CandidateSkillOptions(TranslationOptions):
    fields = ("name",)


@register(CandidateEducation)
class CandidateEducationOptions(TranslationOptions):
    fields = ("title", "from_to", "description")


@register(CandidateExperience)
class CandidateExperienceOptions(TranslationOptions):
    fields = ("job_title", "from_to", "description")
