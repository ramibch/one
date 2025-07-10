import io
import os
import uuid
from copy import copy

from auto_prefetch import ForeignKey
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.gis.db.models import PolygonField
from django.core.files.base import ContentFile
from django.db import models
from django.db.models import Max, Value
from django.db.models.functions import Concat
from django.urls import reverse, reverse_lazy
from django.utils.functional import cached_property
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from pdf2image import convert_from_bytes

from one.choices import CompetenceLevel, Genders, NotificationFrequency, SkillType
from one.companies.models import Person
from one.db import ChoiceArrayField, OneModel, TranslatableModel
from one.tex.compile import render_pdf
from one.tex.values import TEX_LANGUAGE_MAPPING, PaperUnits
from one.tmp import TmpFile

User = get_user_model()


class Candidate(TranslatableModel):
    def get_upload_path(self, filename):
        return f"candidates/{self.id}/{filename}"

    LANG_ATTR = "language"
    LANGS_ATTR = "languages"
    language = models.CharField(
        verbose_name=_("Main language"),
        max_length=4,
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE,
        db_index=True,
    )
    languages = ChoiceArrayField(
        models.CharField(max_length=8, choices=settings.LANGUAGES),
        default=list,
        blank=True,
        db_index=True,
    )
    id = models.UUIDField(
        primary_key=True,
        db_index=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    full_name = models.GeneratedField(
        expression=Concat("first_name", Value(" "), "last_name"),
        output_field=models.CharField(max_length=128),
        db_persist=True,
    )
    job_title = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    phone = models.CharField(max_length=32)
    location = models.CharField(max_length=32)
    linkedin_url = models.CharField(
        verbose_name=_("linkedin URL"),
        max_length=128,
        null=True,
        blank=True,
    )
    website_url = models.URLField(
        verbose_name=_("website URL"),
        max_length=128,
        blank=True,
        null=True,
    )
    about = models.TextField(
        verbose_name=_("about me"),
        null=True,
        blank=True,
    )
    coverletter_body = models.TextField(null=True, blank=True)

    photo = models.ImageField(upload_to=get_upload_path, null=True)
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
            "experience_set",
            "education_set",
            "skill_set",
            "certificate_set",
            "project_set",
            "language_set",
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
    name = models.CharField(max_length=64)
    level = models.IntegerField(choices=CompetenceLevel)
    skill_type = models.CharField(max_length=32, null=True, choices=SkillType)

    @cached_property
    def hx_edit_url(self):
        return reverse_lazy("candidateskill_edit", kwargs=self.get_url_kwargs())

    @cached_property
    def hx_delete_url(self):
        return reverse_lazy("candidateskill_delete", kwargs=self.get_url_kwargs())

    def __str__(self):
        return self.name


class CandidateEducation(CandidateChild):
    institution = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    start_date = models.CharField(max_length=64)
    end_date = models.CharField(max_length=64, null=True, blank=True)
    studying_now = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)

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
    company_name = models.CharField(max_length=64)
    job_title = models.CharField(max_length=64)
    start_date = models.CharField(max_length=64)
    end_date = models.CharField(max_length=64, null=True, blank=True)
    here_now = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)

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
    name = models.CharField(max_length=255)
    query = models.CharField(max_length=255)
    area = PolygonField()
    notification = models.CharField(
        default=NotificationFrequency.WEEKLY, choices=NotificationFrequency
    )
    languages = ChoiceArrayField(
        models.CharField(max_length=8, choices=settings.LANGUAGES),
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


class TexCv(OneModel):
    def get_upload_path(self, filename):
        return f"candidates/{self.candidate.id}/cv_{self.id}/{filename}"

    id = models.UUIDField(
        primary_key=True,
        db_index=True,
        default=uuid.uuid4,
        editable=False,
    )
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
        self.cv_pdf.delete(save=False)
        lang = get_language()
        tex_lang = TEX_LANGUAGE_MAPPING.get(lang)
        context = {"profile": self.candidate, "tex_lang": tex_lang}
        # pdf and tex
        pdf, text = render_pdf(self.template, context, interpreter=self.interpreter)
        self.cv_pdf.save("CV.pdf", ContentFile(pdf), save=False)
        self.cv_text = text
        # image
        img = convert_from_bytes(pdf_file=pdf, first_page=1, last_page=1, fmt="jpg")[0]
        img_buffer = io.BytesIO()
        img.save(img_buffer, format="JPEG")
        self.cv_image.save("CV.jpg", ContentFile(img_buffer.getvalue()), save=False)
        self.save()


class JobApplication(OneModel):
    def get_upload_path(self, filename):
        return f"candidates/{self.cv.candidate.id}/apps/{filename}"

    id = models.UUIDField(
        primary_key=True,
        db_index=True,
        default=uuid.uuid4,
        editable=False,
    )
    cv = ForeignKey(TexCv, on_delete=models.CASCADE)
    candidate = ForeignKey(Candidate, on_delete=models.CASCADE)
    job = ForeignKey("companies.Job", on_delete=models.CASCADE)
    coverletter = models.FileField(upload_to=get_upload_path, null=True, blank=True)
    coverletter_text = models.TextField(null=True, blank=True)
    dossier = models.FileField(upload_to=get_upload_path, null=True, blank=True)
    dossier_text = models.TextField(null=True, blank=True)

    def render_coverletter(self):
        self.coverletter.delete(save=False)
        template = "candidates/tex/coverletter.tex"
        context = {"profile": self.cv.candidate, "job": self.job, "app": self}
        cl_bytes, latex_text = render_pdf(template, context, interpreter="pdflatex")
        self.coverletter.save(_("Coverletter.pdf"), ContentFile(cl_bytes), save=False)
        self.coverletter_text = latex_text
        self.save()

    def render_dossier(self):
        self.dossier.delete(save=False)
        template = "candidates/tex/dossier.tex"
        lang = get_language()
        tex_lang = TEX_LANGUAGE_MAPPING.get(lang)
        context = {
            "profile": self.cv.candidate,
            "job": self.job,
            "app": self,
            "tex_lang": tex_lang,
        }
        cl_bytes, latex_text = render_pdf(template, context, interpreter="pdflatex")
        filename = f"{_('Dossier')}_{lang}.pdf"
        self.dossier.save(filename, ContentFile(cl_bytes), save=False)
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


def get_candidate_child_model(model_name):
    """23.06.2025 not planned to be used (but just in case)"""
    d = {m._meta.model_name: m for m in CandidateChild.__subclasses__()}
    if model_name not in d:
        raise ValueError(f"'{model_name}' is not recognised as a candidate child model")

    return d[model_name]
