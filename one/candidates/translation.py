from modeltranslation.translator import TranslationOptions, register

from .models import CandidateProfile


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
