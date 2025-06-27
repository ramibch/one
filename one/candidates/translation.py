from modeltranslation.translator import TranslationOptions, register

from .models import (
    Candidate,
    CandidateEducation,
    CandidateExperience,
    CandidateSkill,
)


@register(Candidate)
class CandidateOptions(TranslationOptions):
    fields = ("job_title", "location", "about", "coverletter_body")


@register(CandidateSkill)
class CandidateSkillOptions(TranslationOptions):
    fields = ("name",)


@register(CandidateEducation)
class CandidateEducationOptions(TranslationOptions):
    fields = ("title", "description")


@register(CandidateExperience)
class CandidateExperienceOptions(TranslationOptions):
    fields = ("job_title", "description")
