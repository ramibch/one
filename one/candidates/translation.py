from modeltranslation.translator import TranslationOptions, register

from .models import (
    Candidate,
    CandidateEducation,
    CandidateExperience,
    CandidateSkill,
    JobApplication,
    TexCv,
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


@register(TexCv)
class TexCvOptions(TranslationOptions):
    fields = ("cv_text", "cv_image", "cv_pdf")


@register(JobApplication)
class JobApplicationOptions(TranslationOptions):
    fields = ("coverletter", "coverletter_text", "dossier", "dossier_text")
