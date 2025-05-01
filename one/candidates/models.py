from auto_prefetch import ForeignKey, Model
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.db.models import Max
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _


class CandidateProfile(Model):  # TODO: Check TranslatableModel?
    lang = models.CharField(max_length=8, choices=settings.LANGUAGES, default="de")
    position = ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    locations = models.ManyToManyField(Location)
    fullname = models.CharField(max_length=64)
    job_title = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    phone = models.CharField(max_length=32)
    location = models.CharField(max_length=32, null=True, blank=True)
    linkedin = models.CharField(max_length=32, null=True, blank=True)
    github = models.CharField(max_length=32, null=True, blank=True)
    website_label = models.CharField(max_length=64, null=True, blank=True)
    website_url = models.URLField(max_length=128, blank=True, null=True)
    is_rami = models.BooleanField(default=True)
    telegram_chat_id = models.CharField(max_length=32, null=True, blank=True)

    letter_body = models.TextField(help_text="use #company_name, #job_title")
    about = models.TextField(null=True, blank=True)

    why_me = models.CharField(
        max_length=128, default=_("Why Should You Hire Me?"), null=True, blank=True
    )

    latex_pt = models.PositiveSmallIntegerField(default=12)
    photo_width = models.CharField(max_length=3, default="0.7")
    margin_left = models.CharField(max_length=5, default="25mm")
    margin_right = models.CharField(max_length=5, default="20mm")
    margin_top = models.CharField(max_length=5, default="20mm")
    margin_bottom = models.CharField(max_length=5, default="20mm")

    # labels
    about_label = models.CharField(max_length=32, default=_("Professional Profile"))
    experience_label = models.CharField(max_length=32, default=_("Work Experience"))
    education_label = models.CharField(max_length=32, default=_("Education"))
    skill_label = models.CharField(max_length=32, default=_("Technical Skills"))
    certificate_label = models.CharField(max_length=32, default=_("Certifications"))
    language_label = models.CharField(max_length=32, default=_("Languages"))
    project_label = models.CharField(max_length=32, default=_("Projects"))

    signature = models.ImageField(upload_to=upload_job_media, null=True)
    photo = models.ImageField(upload_to=upload_job_media, null=True)
    docs = models.FileField(upload_to=upload_job_media, null=True, blank=True)

    @cached_property
    def has_website(self):
        return self.website_label is not None and self.website_url is not None

    @cached_property
    def first_name(self):
        try:
            return self.fullname.split(" ")[0]
        except KeyError:
            return ""

    @cached_property
    def email_delete_url(self):
        # TODO: WEBSITE_URL ?? site url?
        return settings.WEBSITE_URL + reverse(
            "profile-delete", kwargs={"id": self.id}, query={"email": self.email}
        )

    @cached_property
    def admin_url(self):
        # the url to the Django admin form for the model instance
        info = (self._meta.app_label, self._meta.model_name)
        return reverse("admin:%s_%s_change" % info, args=(self.pk,))

    @cached_property
    def full_admin_url(self):
        return settings.WEBSITE_URL + self.admin_url

    @cached_property
    def cleaned_phone(self):
        return self.phone.replace(" ", "")

    @cached_property
    def cleaned_fullname(self):
        return self.fullname.replace(" ", "")

    @cached_property
    def local_signature_path(self) -> Path:
        return write_local_file(self.signature.name)

    @cached_property
    def local_docs_path(self) -> Path:
        return write_local_file(self.docs.name)

    @cached_property
    def local_photo_path(self) -> Path:
        return write_local_file(self.photo.name)

    def signature_file_exists(self):
        return bool(self.signature.name) and self.signature.storage.exists(
            self.signature.name
        )

    def photo_file_exists(self):
        return bool(self.photo.name) and self.photo.storage.exists(self.photo.name)

    def docs_file_exists(self):
        return bool(self.docs.name) and self.docs.storage.exists(self.docs.name)

    def _clone_children(self, profile_clone):
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
                child.profile = profile_clone
                child.save()

    def clone_obj(self, attrs={}):
        clone = copy(self)
        clone.signature = None
        clone.photo = None
        clone.docs = None
        clone.pk = CandidateProfile.objects.aggregate(Max("id"))["id__max"] + 1

        for key, value in attrs.items():
            setattr(clone, key, value)

        if self.signature_file_exists():
            clone.signature.save(
                os.path.basename(self.signature.name),
                ContentFile(self.signature.read()),
                save=False,
            )

        if self.photo_file_exists():
            clone.photo.save(
                os.path.basename(self.photo.name),
                ContentFile(self.photo.read()),
                save=False,
            )
        if self.docs_file_exists():
            clone.docs.save(
                os.path.basename(self.docs.name),
                ContentFile(self.docs.read()),
                save=False,
            )

        clone.save()

        self._clone_children(clone)

    def __str__(self) -> str:
        return f"{self.fullname} - {self.job_title}"


class CandidateChildrenModel(Model):
    profile = ForeignKey(CandidateProfile, on_delete=models.CASCADE)

    class Meta(Model.Meta):
        abstract = True


class CandidateExperience(CandidateChildrenModel):
    company_name = models.CharField(max_length=64)
    job_title = models.CharField(max_length=64)
    from_to = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.job_title} - {self.company_name}"


class Education(CandidateChildrenModel):
    institution_name = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    from_to = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.institution_name}"


class Skill(CandidateChildrenModel):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Certificate(CandidateChildrenModel):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Project(CandidateChildrenModel):
    title = models.CharField(max_length=64)
    url = models.URLField(max_length=128, null=True, blank=True)
    from_to = models.CharField(max_length=32, null=True, blank=True)
    description = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return self.title


class LanguageSkill(CandidateChildrenModel):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


def cv_upload_path(cv, filename):
    return f"profiles-{cv.profile.category}/{now.year}/{now.month}/{now.day}/{cv.profile.id}/{cv.tex.id}/{filename}"


class TexTemplate(models.TextChoices):
    ALICE = "tex/cvs/alice/cv.tex", "Alice"
    ## TODO: add


class CandidateCv(Model):
    profile = ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    tex_template = models.CharField(max_length=64, choices=TexTemplate)
    rendered_text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=cv_upload_path)
    pdf = models.FileField(upload_to=cv_upload_path)
    pdf_time = models.FloatField(default=0)
    image_time = models.FloatField(default=0)
    rendering_time = models.FloatField(default=0)
    auto_created = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def render_files(self):
        pdf_start = time.time()
        # rendering pdf file
        template = get_template(self.tex.template_name, using="tex")
        self.rendered_text = template.render({"profile": self.profile})
        with tempfile.TemporaryDirectory() as tempdir:
            temppath = Path(tempdir)
            filename = "texput.tex"
            with open(temppath / filename, "x", encoding="utf-8") as f:
                f.write(self.rendered_text)
            args = f"{self.tex.interpreter} -interaction=batchmode {self.tex.interpreter_options} {filename} 2>&1 > /dev/null"
            try:
                run(args, shell=True, stdout=PIPE, stderr=PIPE, check=True, cwd=tempdir)
            except CalledProcessError as called_process_error:
                try:
                    with open(temppath / "texput.log", encoding="utf-8") as f:
                        log = f.read()
                except FileNotFoundError:
                    raise called_process_error
                else:
                    raise TexError(
                        log=log,
                        source=self.rendered_text,
                        template_name=self.tex.template_name,
                    )
            with open(temppath / "texput.pdf", "rb") as f:
                bytes_pdf = f.read()

            filename = f"CV_{now.hour}{now.minute}{now.second}{now.microsecond}"

            self.pdf.save(
                f"{filename}.pdf",
                ContentFile(bytes_pdf),
                save=False,
            )
            # pdf time calculations
            pdf_end = time.time()
            self.pdf_time = pdf_end - pdf_start
            # create the image  file
            image = convert_from_path(
                pdf_path=temppath / "texput.pdf",
                first_page=1,
                last_page=1,
                fmt="jpg",
                output_folder=temppath,
            )[0]
            with open(image.filename, "rb") as f:
                self.image.save(
                    f"{filename}.jpg",
                    ContentFile(f.read()),
                    save=False,
                )
            # total and image time calculations
            self.image_time = time.time() - pdf_end
            self.rendering_time = self.image_time + self.pdf_time

            self.save()

        return self

    def __str__(self) -> str:
        return f"CV ({self.profile.fullname} {self.tex})"

    class Meta(Model.Meta):
        ordering = ["-created_on"]
