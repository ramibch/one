import io
import os
import uuid
from copy import copy

from auto_prefetch import ForeignKey
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.gis.db.models import PolygonField
from django.core.files.base import ContentFile
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Value
from django.db.models.functions import Concat
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from pdf2image import convert_from_bytes

from one.choices import Genders
from one.companies.models import Person
from one.db import ChoiceArrayField, OneModel, TranslatableModel
from one.tex.compile import render_pdf
from one.tex.values import TEX_LANGUAGE_MAPPING, PaperUnits
from one.tmp import TmpFile

User = get_user_model()


class CandidateProfile(TranslatableModel):
    def get_upload_path(self, filename):
        return f"candidates/{self.id}/{filename}"

    LANG_ATTR = "language"
    LANGS_ATTR = "languages"
    language = models.CharField(
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
    gender = models.CharField(max_length=64, choices=Genders, null=True, blank=True)
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
    linkedin_url = models.CharField(max_length=128, null=True, blank=True)
    website_url = models.URLField(max_length=128, blank=True, null=True)
    about = models.TextField(null=True, blank=True)
    coverletter_body = models.TextField(null=True, blank=True)

    # labels
    about_label = models.CharField(max_length=32, default=_("Professional Profile"))
    experience_label = models.CharField(max_length=32, default=_("Work Experience"))
    education_label = models.CharField(max_length=32, default=_("Education"))
    skill_label = models.CharField(max_length=32, default=_("Technical Skills"))
    certificate_label = models.CharField(max_length=32, default=_("Certifications"))
    language_label = models.CharField(max_length=32, default=_("Languages"))
    project_label = models.CharField(max_length=32, default=_("Projects"))

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
                child.profile = cloned_obj
                child.save()

    def get_absolute_url(self):
        return reverse("candidateprofile_detail", kwargs={"pk": self.pk})

    @cached_property
    def url(self):
        return self.get_absolute_url()

    @cached_property
    def edit_url(self):
        return reverse("candidateprofile_edit", kwargs={"pk": self.pk})


class CandidateProfileChild(TranslatableModel):
    LANG_ATTR = "profile__language"
    LANGS_ATTR = "profile__languages"
    profile = ForeignKey(CandidateProfile, on_delete=models.CASCADE)

    class Meta(TranslatableModel.Meta):
        abstract = True


class NotificationTypes(models.TextChoices):
    DAILY = "daily", _("Daily")
    WEEKLY = "weekly", _("Weekly")
    NONE = "none", _("No notification")


class CandidateJobAlert(CandidateProfileChild):
    name = models.CharField(max_length=255)
    query = models.CharField(max_length=255)
    area = PolygonField()
    notification = models.CharField(
        default=NotificationTypes.WEEKLY, choices=NotificationTypes
    )
    languages = ChoiceArrayField(
        models.CharField(max_length=8, choices=settings.LANGUAGES),
        default=list,
        blank=True,
        db_index=True,
    )


class CandidateExperience(CandidateProfileChild):
    company_name = models.CharField(max_length=64)
    job_title = models.CharField(max_length=64)
    from_to = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.job_title} - {self.company_name}"


class CandidateEducation(CandidateProfileChild):
    institution_name = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    from_to = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.institution_name}"


class CandidateSkill(CandidateProfileChild):
    name = models.CharField(max_length=64)
    level = models.PositiveSmallIntegerField(
        default=3, validators=[MaxValueValidator(100), MinValueValidator(0)]
    )

    def __str__(self):
        return self.name


class CandidateCertificate(CandidateProfileChild):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class CandidateProject(CandidateProfileChild):
    title = models.CharField(max_length=64)
    url = models.URLField(max_length=128, null=True, blank=True)
    from_to = models.CharField(max_length=32, null=True, blank=True)
    description = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return self.title


class CandidateLanguageSkill(CandidateProfileChild):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


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
        return f"candidates/{self.profile.id}/cvs/{filename}"

    id = models.UUIDField(
        primary_key=True,
        db_index=True,
        default=uuid.uuid4,
        editable=False,
    )
    profile = ForeignKey(CandidateProfile, on_delete=models.CASCADE)
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
        return f"CV ({self.profile.full_name})"

    @cached_property
    def interpreter(self) -> str:
        return TexCvTemplates(self.template).interpreter

    def render_cv(self):
        self.cv_pdf.delete(save=False)
        lang = get_language()
        tex_lang = TEX_LANGUAGE_MAPPING.get(lang)
        context = {"profile": self.profile, "tex_lang": tex_lang}
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
        return f"candidates/{self.cv.profile.id}/apps/{filename}"

    id = models.UUIDField(
        primary_key=True,
        db_index=True,
        default=uuid.uuid4,
        editable=False,
    )
    cv = ForeignKey(TexCv, on_delete=models.CASCADE)
    job = ForeignKey("companies.Job", on_delete=models.CASCADE)
    coverletter = models.FileField(upload_to=get_upload_path, null=True, blank=True)
    coverletter_text = models.TextField(null=True, blank=True)
    dossier = models.FileField(upload_to=get_upload_path, null=True, blank=True)
    dossier_text = models.TextField(null=True, blank=True)

    def render_coverletter(self):
        self.coverletter.delete(save=False)
        template = "candidates/tex/coverletter.tex"
        context = {"profile": self.cv.profile, "job": self.job, "app": self}
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
            "profile": self.cv.profile,
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
