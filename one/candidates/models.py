import io
import os
import uuid
from copy import copy

from auto_prefetch import ForeignKey, OneToOneField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.gis.db.models import PolygonField
from django.core.files.base import ContentFile
from django.db import models
from django.db.models import Max, Value
from django.db.models.functions import Concat
from django.urls import reverse, reverse_lazy
from django.utils import translation
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from pdf2image import convert_from_bytes

from one.choices import CompetenceLevel, Genders, NotificationFrequency, SkillType
from one.companies.models import Person
from one.db import ChoiceArrayField, OneModel, TranslatableModel
from one.tex.compile import render_pdf_and_text
from one.tex.values import TEX_LANGUAGE_MAPPING, PaperUnits
from one.tmp import TmpFile

User = get_user_model()


class Candidate(TranslatableModel):
    def get_upload_path(self, filename):
        return f"candidates/{self.id}/{filename}"

    LANG_ATTR = "language"
    LANGS_ATTR = "languages"
    language = models.CharField(
        verbose_name=_("Primary language"),
        max_length=4,
        choices=settings.LANGUAGES,
    )
    languages = ChoiceArrayField(
        models.CharField(max_length=8, choices=settings.LANGUAGES),
        verbose_name=_("Additional Languages"),
        default=list,
        blank=True,
    )
    id = models.UUIDField(
        primary_key=True,
        db_index=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=64, verbose_name=_("First name"))
    last_name = models.CharField(max_length=64, verbose_name=_("Last name"))
    full_name = models.GeneratedField(
        expression=Concat("first_name", Value(" "), "last_name"),
        output_field=models.CharField(max_length=128),
        verbose_name=_("Full name"),
        db_persist=True,
    )
    job_title = models.CharField(max_length=64, verbose_name=_("Job title"))
    email = models.EmailField(max_length=64, verbose_name=_("E-mail"))
    phone = models.CharField(max_length=32, verbose_name=_("Phone number"))
    location = models.CharField(max_length=32, verbose_name=_("Location"))
    linkedin_url = models.CharField(
        verbose_name=_("LinkedIn URL"),
        max_length=128,
        null=True,
        blank=True,
    )
    website_url = models.URLField(
        verbose_name=_("Website URL"),
        max_length=128,
        blank=True,
        null=True,
    )
    about = models.TextField(
        verbose_name=_("About me"),
        null=True,
        blank=True,
    )
    coverletter_body = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Body of cover letter"),
    )

    photo = models.ImageField(
        upload_to=get_upload_path,
        null=True,
        verbose_name=_("Photo"),
    )
    docs = models.FileField(upload_to=get_upload_path, null=True, blank=True)

    own_cv = models.FileField(upload_to=get_upload_path, null=True, blank=True)
    receive_job_alerts = models.BooleanField(default=True)
    is_public = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.full_name} - {self.job_title}"

    @cached_property
    def local_photo_path(self) -> str:
        return str(TmpFile(self.photo).path)

    @cached_property
    def photo_file_exists(self) -> bool:
        return bool(self.photo.name) and self.photo.storage.exists(self.photo.name)

    @cached_property
    def linkedin(self) -> str:
        if self.linkedin_url is None:
            return ""
        url: str = self.linkedin_url
        index = -2 if url.endswith("/") else -1
        return url.split("/")[index]

    @cached_property
    def website(self) -> str:
        if not self.website_url:
            return ""
        url: str = self.website_url
        url.removesuffix("/")
        for prefix in ("https://www.", "https://", "http://www.", "http://"):
            if url.startswith(prefix):
                return url.removeprefix(prefix)
        return url

    def clone_obj(self, attrs: dict):
        clone = copy(self)
        clone.photo = None
        for key, value in attrs.items():
            setattr(clone, key, value)
        if self.photo_file_exists:
            clone.photo.save(
                os.path.basename(self.photo.name),
                ContentFile(self.photo.read()),
                save=False,
            )
        clone.save()
        self._clone_children(clone)

    def _clone_children(self, cloned_obj):
        related_sets = (
            "candidateexperience_set",
            "candidateeducation_set",
            "candidateskill_set",
        )
        for related_set in related_sets:
            children_related = getattr(self, related_set, None)
            if children_related is None:
                continue
            for child in children_related.all():
                child.pk = None
                child.candidate = cloned_obj
                child.save()

    def get_absolute_url(self):
        return reverse("candidate_detail", kwargs={"pk": self.pk})

    @cached_property
    def url(self):
        return self.get_absolute_url()

    @cached_property
    def edit_url(self):
        return reverse("candidate_edit", kwargs={"pk": self.pk})

    @cached_property
    def delete_url(self):
        return reverse("candidate_delete", kwargs={"pk": self.pk})

    @cached_property
    def hx_edit_url(self):
        return reverse("candidateinfo_edit", kwargs={"pk": self.pk})

    @cached_property
    def hx_create_skill_url(self):
        return reverse("candidateskill_create", kwargs={"candidate_pk": self.pk})

    @cached_property
    def hx_skill_order_url(self):
        return reverse("candidateskill_order", kwargs={"candidate_pk": self.pk})

    @cached_property
    def hx_create_education_url(self):
        return reverse("candidateeducation_create", kwargs={"candidate_pk": self.pk})

    @cached_property
    def hx_education_order_url(self):
        return reverse("candidateeducation_order", kwargs={"candidate_pk": self.pk})

    @cached_property
    def hx_create_experience_url(self):
        return reverse("candidateexperience_create", kwargs={"candidate_pk": self.pk})

    @cached_property
    def hx_experience_order_url(self):
        return reverse("candidateexperience_order", kwargs={"candidate_pk": self.pk})


class CandidateChild(TranslatableModel):
    LANG_ATTR = "candidate__language"
    LANGS_ATTR = "candidate__languages"
    candidate = ForeignKey(Candidate, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(null=True)
    id = models.UUIDField(
        primary_key=True,
        db_index=True,
        default=uuid.uuid4,
        editable=False,
    )

    def get_url_kwargs(self) -> dict:
        return {"candidate_pk": self.candidate.pk, "pk": self.pk}

    def save(self, *args, **kwargs):
        if not self.order:
            qs = type(self).objects.filter(candidate=self.candidate)
            max_order = qs.aggregate(Max("order"))["order__max"]
            self.order = max_order + 1 if max_order else 0
        return super().save(*args, **kwargs)

    class Meta(TranslatableModel.Meta):
        abstract = True
        ordering = ("order",)


class CandidateSkill(CandidateChild):
    name = models.CharField(max_length=64, verbose_name=_("Name"))
    level = models.IntegerField(choices=CompetenceLevel, verbose_name=_("Level"))
    skill_type = models.CharField(
        max_length=32,
        null=True,
        choices=SkillType,
        verbose_name=_("Skill type"),
    )

    @cached_property
    def hx_edit_url(self):
        return reverse_lazy("candidateskill_edit", kwargs=self.get_url_kwargs())

    @cached_property
    def hx_delete_url(self):
        return reverse_lazy("candidateskill_delete", kwargs=self.get_url_kwargs())

    @cached_property
    def main_name(self):
        return getattr(self, f"name_{self.candidate.language}")

    def __str__(self):
        return self.name


class CandidateEducation(CandidateChild):
    institution = models.CharField(
        max_length=64,
        verbose_name=_("Institution"),
    )
    title = models.CharField(
        max_length=64,
        verbose_name=_("Title"),
    )
    start_date = models.CharField(
        max_length=64,
        verbose_name=_("Start date"),
    )
    end_date = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name=_("End date"),
    )
    studying_now = models.BooleanField(
        default=False,
        verbose_name=_("Studying this now"),
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Description"),
    )

    @property
    def x_data_end_date(self):
        return "''" if self.end_date is None else f"'{self.end_date}'"

    @property
    def x_data_studying_now(self):
        return "true" if self.studying_now else "false"

    @cached_property
    def hx_edit_url(self):
        return reverse_lazy("candidateeducation_edit", kwargs=self.get_url_kwargs())

    @cached_property
    def hx_delete_url(self):
        return reverse_lazy("candidateeducation_delete", kwargs=self.get_url_kwargs())

    def __str__(self):
        return f"{self.title} - {self.institution}"


class CandidateExperience(CandidateChild):
    company_name = models.CharField(
        max_length=64,
        verbose_name=_("Company name"),
    )
    job_title = models.CharField(
        max_length=64,
        verbose_name=_("Role"),
    )
    start_date = models.CharField(
        max_length=64,
        verbose_name=_("Start date"),
    )
    end_date = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name=_("End date"),
    )
    here_now = models.BooleanField(
        default=False,
        verbose_name=_("Working here now"),
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Description"),
    )

    @property
    def x_data_end_date(self):
        return "''" if self.end_date is None else f"'{self.end_date}'"

    @property
    def x_data_here_now(self):
        return "true" if self.here_now else "false"

    @cached_property
    def hx_edit_url(self):
        return reverse_lazy("candidateexperience_edit", kwargs=self.get_url_kwargs())

    @cached_property
    def hx_delete_url(self):
        return reverse_lazy("candidateexperience_delete", kwargs=self.get_url_kwargs())

    def __str__(self):
        return f"{self.job_title} - {self.company_name}"


class CandidateJobAlert(CandidateChild):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
    )
    query = models.CharField(
        max_length=255,
        verbose_name=_("Term"),
    )
    area = PolygonField(verbose_name=_("Area"))
    notification = models.CharField(
        default=NotificationFrequency.WEEKLY,
        choices=NotificationFrequency,
        verbose_name=_("Notification type"),
    )
    languages = ChoiceArrayField(
        models.CharField(max_length=8, choices=settings.LANGUAGES),
        verbose_name=_("Languages"),
        default=list,
        blank=True,
        db_index=True,
    )


class TexCvTemplates(models.TextChoices):
    ALICE = "candidates/tex/cv_alice.tex", "Alice"
    DEVELOPER = "candidates/tex/cv_developer.tex", "Developer"
    FREEMAN = "candidates/tex/cv_freeman.tex", "Freeman"
    KRIEGER = "candidates/tex/cv_krieger.tex", "Krieger"
    MARISSA = "candidates/tex/cv_marissa.tex", "Marissa"
    MODERN = "candidates/tex/cv_modern.tex", "Modern"
    RECEIVE = "candidates/tex/cv_receive.tex", "Receive"

    @property
    def interpreter(self):
        return {
            self.ALICE: "xelatex",
            self.DEVELOPER: "xelatex",
            self.FREEMAN: "xelatex",
            self.KRIEGER: "xelatex",
            self.MARISSA: "pdflatex",
            self.MODERN: "xelatex",
            self.RECEIVE: "lualatex",
        }[self]


class TexCv(TranslatableModel):
    def get_upload_path(self, filename):
        return f"candidates/{self.candidate.id}/cv_{self.id}/{filename}"

    id = models.UUIDField(
        primary_key=True,
        db_index=True,
        default=uuid.uuid4,
        editable=False,
    )
    LANG_ATTR = "candidate__language"
    LANGS_ATTR = "candidate__languages"
    candidate = ForeignKey(Candidate, on_delete=models.CASCADE)
    template = models.CharField(max_length=64, choices=TexCvTemplates)
    cv_text = models.TextField(null=True, blank=True)
    cv_image = models.ImageField(upload_to=get_upload_path, null=True, blank=True)
    cv_pdf = models.FileField(upload_to=get_upload_path, null=True, blank=True)
    latex_pt = models.PositiveSmallIntegerField(default=12)
    margin_left = models.PositiveSmallIntegerField(default=25)
    margin_right = models.PositiveSmallIntegerField(default=20)
    margin_top = models.PositiveSmallIntegerField(default=20)
    margin_bottom = models.PositiveSmallIntegerField(default=20)
    margin_unit = models.CharField(default=PaperUnits.MILIMITERS, choices=PaperUnits)

    class Meta(OneModel.Meta):
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"CV ({self.candidate.full_name})"

    @cached_property
    def interpreter(self) -> str:
        return TexCvTemplates(self.template).interpreter

    def render_cv(self):
        for lang in self.get_languages():
            cv_pdf = getattr(self, f"cv_pdf_{lang}")
            cv_image = getattr(self, f"cv_image_{lang}")

            cv_pdf.delete(save=False)
            cv_image.delete(save=False)

            with translation.override(lang):
                tex_lang = TEX_LANGUAGE_MAPPING.get(lang)
                context = {"candidate": self.candidate, "tex_lang": tex_lang}
                # pdf and text
                pdf, text = render_pdf_and_text(
                    self.template,
                    context,
                    interpreter=self.interpreter,
                )
                cv_pdf.save(f"CV_{lang}.pdf", ContentFile(pdf), save=False)

                # text
                setattr(self, f"cv_text_{lang}", text)

                # image
                img = convert_from_bytes(
                    pdf_file=pdf,
                    first_page=1,
                    last_page=1,
                    fmt="jpg",
                )[0]
                img_buffer = io.BytesIO()
                img.save(img_buffer, format="JPEG")
                img_bytes = img_buffer.getvalue()
                cv_image.save(f"CV_{lang}.jpg", ContentFile(img_bytes), save=False)
        self.save()


COMMON_TEX_CONTEXT = {
    "about_label": _("About me"),
    "hard_skills_label": _("Hard skills"),
    "soft_skills_label": _("Soft skills"),
    "languages_label": _("Languages"),
    "education_label": _("Education"),
    "experience_label": _("Experience"),
    "now_label": _("Now"),
}


class JobApplication(OneModel):
    def get_upload_path(self, filename):
        return f"candidates/{self.candidate.id}/apps/{filename}"

    id = models.UUIDField(
        primary_key=True,
        db_index=True,
        default=uuid.uuid4,
        editable=False,
    )
    language = models.CharField(
        verbose_name=_("Language"),
        max_length=4,
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE,
    )
    job = ForeignKey(
        "companies.Job",
        on_delete=models.CASCADE,
        verbose_name=_("Job"),
    )
    candidate = ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        verbose_name=_("Candidate"),
    )
    # Application option 1: cv + coverletter (complex, to be defined)
    cv = ForeignKey(
        TexCv,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Curriculum Vitae"),
    )
    coverletter = models.FileField(
        upload_to=get_upload_path,
        null=True,
        blank=True,
        verbose_name=_("Cover letter"),
    )
    coverletter_text = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("LaTeX text of Cover letter"),
    )
    # Application option 2: dossier (easier to implement)
    dossier = models.FileField(
        upload_to=get_upload_path,
        null=True,
        blank=True,
        verbose_name=_("Dossier"),
    )
    dossier_text = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("LaTeX text of Dossier"),
    )

    def render_coverletter(self):
        self.coverletter.delete(save=False)
        template = "candidates/tex/coverletter.tex"
        context = {
            "candidate": self.candidate,
            "job": self.job,
            "app": self,
        }
        cl_bytes, latex_text = render_pdf_and_text(
            template, context, interpreter="pdflatex"
        )
        self.coverletter.save(_("Coverletter.pdf"), ContentFile(cl_bytes), save=False)
        self.coverletter_text = latex_text
        self.save()

    def render_dossier(self):
        self.dossier.delete(save=False)
        with translation.override(self.language):
            hard_skills = CandidateSkill.objects.filter(
                candidate=self.candidate,
                skill_type=SkillType.HARD,
            )
            soft_skills = CandidateSkill.objects.filter(
                candidate=self.candidate,
                skill_type=SkillType.SOFT,
            )
            language_skills = CandidateSkill.objects.filter(
                candidate=self.candidate,
                skill_type=SkillType.LANGUAGE,
            )
            skills_cols = sum(
                CandidateSkill.objects.filter(
                    candidate=self.candidate, skill_type=skill_type
                ).exists()
                for skill_type in SkillType.values
            )

            context = {
                "candidate": self.candidate,
                "hard_skills": hard_skills,
                "soft_skills": soft_skills,
                "language_skills": language_skills,
                "skills_cols": skills_cols,
                "job": self.job,
                "app": self,
                "tex_lang": TEX_LANGUAGE_MAPPING.get(self.language),
            } | COMMON_TEX_CONTEXT

            d_bytes, latex_text = render_pdf_and_text(
                "candidates/tex/dossier.tex",
                context,
                interpreter="pdflatex",
            )

            self.dossier.save(f"{_('Dossier')}.pdf", ContentFile(d_bytes), save=False)
            self.dossier_text = latex_text
            self.save()

    @cached_property
    def coverletter_title(self):
        return f"{_('Job application')}: {self.job.title}"

    @cached_property
    def coverletter_salutation(self):
        recruiter: Person = self.job.recruiter
        if recruiter is None:
            return _("Dear Sir/Madam")
        else:
            gender = _("Mrs") if recruiter.gender == Genders.FEMALE else _("Mr")
            return f"{_('Dear')} {gender} {recruiter.last_name}"

    @cached_property
    def coverletter_closing(self):
        return _("Best regards")

    @cached_property
    def hx_delete_url(self):
        return reverse_lazy("jobapplication_delete", kwargs={"pk": self.pk})
