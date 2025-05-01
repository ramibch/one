import io
from copy import copy
from pathlib import Path
from urllib.parse import urlencode

import auto_prefetch
from content.models import Topic
from django.conf import settings
from django.core.files import File
from django.core.mail import EmailMessage
from django.db import models
from django.urls import reverse
from django.utils import timezone, translation
from django.utils.functional import cached_property
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from pdfrw import PdfReader, PdfWriter
from socialmedia.models import FacebookGroup, LinkedinGroup
from socialmedia.tasks import create_linkedin_post
from tex.compile import render_pdf as latex_render_pdf
from tex.values import LATEX_LANGUAGES
from utils.files import write_local_file
from utils.telegram import report_to_admin
from utils.webdrivers import Facebook, SMSSender


def upload_job_media(obj, filename):
    return f"jobs/{slugify(obj._meta.verbose_name_plural)}/{obj.id}/{filename}"


class Location(auto_prefetch.Model):
    name = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.name


class Position(auto_prefetch.Model):
    TYPES = (
        ("fulltime", "Fulltime job"),
        ("parttime", "Parttime job"),
        ("tranning", "Apprenticeship"),
    )
    name = models.CharField(max_length=64)
    position_type = models.CharField(max_length=16, choices=TYPES)
    remote = models.BooleanField(default=False)

    def __str__(self) -> str:
        emoji = "💻" if self.remote else "👨‍⚕️"
        return f"{emoji} {self.name} - {self.get_position_type_display()}"


class Company(auto_prefetch.Model):
    name = models.CharField(max_length=64, unique=True)
    address = models.TextField()
    email_allowed = models.BooleanField(default=True)
    remarks = models.TextField(blank=True, null=True)

    @cached_property
    def address_nolines(self):
        return self.address.replace("\n", " ").strip()

    def __str__(self) -> str:
        return self.name


class Recruiter(auto_prefetch.Model):
    GENDERS = (("m", "Male"), ("f", "Female"))
    company = auto_prefetch.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=64)
    gender = models.CharField(max_length=64, choices=GENDERS, null=True, blank=True)
    email = models.EmailField(max_length=64, null=True, blank=True)
    phone = models.CharField(max_length=64, null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta(auto_prefetch.Model.Meta):
        unique_together = [["name", "company"]]

    def __str__(self) -> str:
        return f"{self.name} ({self.company})"


class Job(auto_prefetch.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    lang = models.CharField(max_length=8, choices=settings.LANGUAGES, default="de")
    company = auto_prefetch.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    recruiter = auto_prefetch.ForeignKey(
        Recruiter, on_delete=models.SET_NULL, null=True
    )
    position = auto_prefetch.ForeignKey(Position, on_delete=models.CASCADE, null=True)
    location = auto_prefetch.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=64)
    extern_id = models.CharField(max_length=32, blank=True, null=True)
    url = models.URLField(max_length=128, blank=True, null=True)
    promoted = models.BooleanField(default=False)
    topics = models.ManyToManyField(
        Topic, help_text="For promotion purposes", blank=True
    )

    def __str__(self) -> str:
        return self.title

    def email_apply_url(self, profile):
        return (
            settings.WEBSITE_URL
            + reverse("job-apply", kwargs={"profile_id": profile.id, "job_id": self.id})
            + "?"
            + urlencode({"email": profile.email})
        )

    def recommend_to_profile(self, profile):
        body = f"Hey {profile.first_name}\n\n"
        with translation.override(profile.lang):
            body += _("This job may be of interest to you") + ":\n"
            body += f"{self.title}\n"
            if self.url:
                body += f"{self.url}\n"
            body += _("Company") + f": {self.company.name}\n\n"
            body += _("If you want me to apply for you, click on next link") + ":"
            body += f"\n{self.email_apply_url(profile)}\n\n"
            body += _("Best regards")
            body += "\nRami"
            body += "\n\n\n"
            body += _("You can delete your data from my site anytime")
            body += f":\n{profile.email_delete_url}"

            message = EmailMessage(
                subject=self.title + " - " + self.company.name,
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[profile.email],
            )
            message.send()

    def promote(self):
        with translation.override(self.lang):
            reporting = f"Promoting job: {self.title}\n"

            # Promote in Facebook
            try:
                reporting += self.promote_in_facebook()
            except Exception as e:
                reporting += f"❌ Error promoting in Facebook: {e}\n"

            # Promote in Linkedin
            try:
                reporting += self.promote_in_linkedin()
            except Exception as e:
                reporting += f"❌ Error promoting in Linkedin: {e}\n"

            # Report to admin
            report_to_admin(reporting)
            # Save state in db
            self.promoted = True
            self.save()

    def promote_in_facebook(self) -> str:
        groups = FacebookGroup.objects.filter(
            topics__in=self.topics.all(), language=self.lang, active=True
        ).distinct()

        if groups.count() == 0:
            return "⚠️ No Facebooks groups found to promote\n"

        fb = Facebook()
        out = "Facebook:\n"
        for index, fb_group in enumerate(groups, start=1):
            try:
                fb.post_in_group(
                    self.get_promotion_text(),
                    group_id=fb_group.group_id,
                    close_driver=index == groups.count(),
                )
                out += f"✔ Posted in facebook group {fb_group.url}\n"
            except Exception as e:
                out += f"❌ Exception in  facebook group: {e}\n"
                if index == groups.count():
                    fb.driver.close()

        return out

    def promote_in_linkedin(self):
        groups = LinkedinGroup.objects.filter(
            topics__in=self.topics.all(), language=self.lang, active=True
        ).distinct()

        if groups.count() == 0:
            return "⚠️ No Linkedin groups found to promote\n"

        post = create_linkedin_post(self.get_promotion_text())
        out = "Linkedin:\n"
        for li_group in groups:
            try:
                post.share(visibility=li_group.visibility, container=li_group.container)
                out += f"✔ Posted in Linkedin group {li_group.url}\n"
            except Exception as e:
                out += f"❌ Exception in  Linkedin group: {e}\n"
        return out

    def get_promotion_text(self):
        out = _("Hi everyone!") + "\n"
        out += self.company.name + " " + _("has published a new job") + ":\n"
        out += self.title + "\n"
        out += self.url + "\n"
        out += _("Company") + f": {self.company.name} \n\n"
        out += _(
            "If you want to apply, I can help you create a nice application dossier for free, so you have more chances of getting the job. Just write to me a Message."
        )
        return out


class Application(auto_prefetch.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    profile = auto_prefetch.ForeignKey(Profile, on_delete=models.CASCADE)
    job = auto_prefetch.ForeignKey(Job, on_delete=models.CASCADE)
    draft = models.BooleanField(default=False)
    candidate_informed = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)
    email_sent_on = models.DateTimeField(null=True, blank=True)
    email_subject = models.CharField(max_length=128, blank=True, null=True)
    email_body = models.TextField(blank=True, null=True)
    sms_sent = models.BooleanField(default=False)
    sms_sent_on = models.DateTimeField(null=True, blank=True)

    remarks = models.TextField(blank=True, null=True)

    why_me_description = models.TextField(null=True, blank=True)

    dossier = models.FileField(upload_to=upload_job_media, null=True, blank=True)
    letter = models.FileField(upload_to=upload_job_media, null=True, blank=True)
    cv = models.FileField(upload_to=upload_job_media, null=True, blank=True)

    class Meta(auto_prefetch.Model.Meta):
        unique_together = [["profile", "job"]]

    def __str__(self):
        return f"{self.job.title} ({self.job.company.name})"

    @cached_property
    def local_dossier_path(self) -> Path:
        return write_local_file(self.dossier.name)

    @cached_property
    def latex_lang(self):
        return LATEX_LANGUAGES[self.profile.lang]

    def return_file_name(self, d: dict) -> str:
        return f"{d[self.profile.lang]}_{self.profile.cleaned_fullname}.pdf"

    @cached_property
    def dossier_filename(self) -> str:
        d = {"de": "Bewerbungsmappe", "en": "Application-dossier", "es": "Dossier"}
        return self.return_file_name(d)

    @cached_property
    def letter_filename(self) -> str:
        d = {"de": "Anschreiben", "en": "Cover-letter", "es": "Carta-de-motivación"}
        return self.return_file_name(d)

    @cached_property
    def cv_filename(self) -> str:
        d = {"de": "Lebenslauf", "en": "Curriculum-vitae", "es": "Curriculum-vitae"}
        return self.return_file_name(d)

    @cached_property
    def admin_url(self):
        # the url to the Django admin form for the model instance
        info = (self._meta.app_label, self._meta.model_name)
        return reverse("admin:%s_%s_change" % info, args=(self.pk,))

    @cached_property
    def full_admin_url(self):
        return settings.WEBSITE_URL + self.admin_url

    @cached_property
    def title(self):
        d = {
            "de": "Bewerbung um die Stelle",
            "es": "Solicitud para el puesto de",
            "en": "Application for the position of",
        }
        return f"{d[self.profile.lang]} {self.job_title_and_id}"

    @cached_property
    def job_title_and_id(self):
        extra = "" if self.job.extern_id is None else f" ({self.job.extern_id})"
        return f"{self.job.title}" + extra

    @cached_property
    def job_title(self):
        return self.job.title

    @cached_property
    def processed_letter_body(self):
        body = copy(self.profile.letter_body)
        body = body.replace("#job_title", self.job.title)
        body = body.replace("#company_name", self.job.company.name)
        return body

    @cached_property
    def message_closing(self):
        d = {"de": "Freundliche Grüssen", "es": "Saludos", "en": "Best regards"}
        return d[self.profile.lang]

    @cached_property
    def message_salutation(self):
        recruiter_name = self.job.recruiter.name
        recruiter_gender = self.job.recruiter.gender

        if recruiter_name is not None and recruiter_gender in ("f", "m"):
            d = {
                "f": {"en": "Dear Mrs.", "de": "Guten Tag Frau", "es": "Estimada Sra."},
                "m": {"en": "Dear Mr.", "de": "Guten Tag Herr", "es": "Estimado Sr."},
            }
            try:
                name = recruiter_name.split()[1]
            except KeyError:
                name = recruiter_name.split()
            return f"{d[recruiter_gender][self.profile.lang]} {name}"

        d = {
            "de": "Sehr geehrte Damen und Herren",
            "en": "Dear Sir or Madam",
            "es": "Estimado Sr. o Sra",
        }
        return d[self.profile.lang]

    def get_email_subject(self):
        return self.title

    def get_email_body(self):
        body = self.message_salutation + ",\n\n"

        if self.profile.is_rami:
            if self.profile.lang == "de":
                body += f"mit großer Begeisterung habe ich Ihre Stellenausschreibung {self.job_title_and_id} gelesen. "
                body += "Im Anhang dieser E-Mail finden Sie daher meine Bewerbungsunterlagen."
                body += "\n\n"
                body += "Meine langjährige Berufserfahrung qualifiziert mich als idealen Kandidaten für diese Stelle. "
                body += "Weiteren Informationen entnehmen Sie bitte meinen Unterlagen."
                body += "\n\n"
                body += "Gerne stehe ich Ihnen für Rückfragen jederzeit zur Verfügung und freue mich, "
                body += "Sie in einem persönlichen Gespräch von mir zu überzeugen."
                body += "\n\n"
                body += "Vielen Dank."
                body += "\n\n"
            if self.profile.lang == "en":
                body += f"I read your job advertisement {self.job_title_and_id} with great enthusiasm. "
                body += "Please find my application documents attached to this e-mail."
                body += "\n\n"
                body += "My many years of professional experience qualify me as the ideal candidate for this position. "
                body += "Please refer to my documents for further information."
                body += "\n\n"
                body += "I will be happy to answer any questions you may have at any time and look forward to "
                body += "I look forward to convincing you in a personal interview."
                body += "\n\n"
                body += "Thank you very much."
                body += "\n\n"
            if self.profile.lang == "es":
                body += f"He leído su anuncio de empleo {self.job_title_and_id} con gran entusiasmo. "
                body += "Adjunto a este correo electrónico la documentación de mi candidatura."
                body += "\n\n"
                body += "Mis años de experiencia profesional me cualifican como el candidato ideal para este puesto. "
                body += "Por favor, consulte mis documentos para más información."
                body += "\n\n"
                body += "Estaré encantado de responder a cualquier pregunta que pueda tener en cualquier momento y espero "
                body += "Espero poder convencerle en una entrevista personal."
                body += "\n\n"
                body += "Muchas gracias"
                body += "\n\n"

        else:
            if self.profile.lang == "de":
                body += f"{self.profile.fullname} ist an der Stelle {self.job_title_and_id} interessiert. "
                body += "Im Anhang dieser E-Mail finden Sie die Bewerbungsunterlagen."
                body += "\n\n"
                body += "Gerne stehen wir Ihnen für Rückfragen jederzeit zur Verfügung."
                body += "\n\n"
                body += "Vielen Dank."
                body += "\n\n"
            if self.profile.lang == "en":
                body += f"{self.profile.fullname} is interested in the job {self.job_title_and_id}. "
                body += "Please find the application documents attached to this e-mail."
                body += "\n\n"
                body += "We are happy to answer any questions you may have at any time."
                body += "\n\n"
                body += "Thank you very much."
                body += "\n\n"
            if self.profile.lang == "es":
                body += f"{self.profile.fullname}, tiene interés en el puesto de {self.job_title_and_id}. "
                body += "Adjunta a este correo electrónico encontrará la documentación de la candidatura."
                body += "\n\n"
                body += "Estaremos encantados de responder a cualquier pregunta que pueda tener en cualquier momento."
                body += "\n\n"
                body += "Muchas gracias."
                body += "\n\n"

        body += f"{self.message_closing},\nRami Boutassghount | www.nicecv.online"

        return body

    @cached_property
    def allow_to_send_email(self) -> bool:
        return all((
            not self.email_sent,
            not self.draft,
            self.job.company.email_allowed,
            self.job.recruiter.email is not None,
            self.dossier is not None,
        ))

    @cached_property
    def allow_to_send_sms_to_recruiter(self) -> bool:
        return all((
            self.recruiter_phone.startswith("+41"),
            self.email_sent,
            self.job.company.email_allowed,
            self.job.recruiter.email is not None,
        ))

    @cached_property
    def allow_to_send_sms_to_candidate(self) -> bool:
        return all((self.candidate_phone.startswith("+41"), self.email_sent))

    @cached_property
    def recruiter_phone(self) -> str:
        if self.job.recruiter.phone is None:
            return ""
        return self.job.recruiter.phone.replace(" ", "")

    @cached_property
    def candidate_phone(self) -> str:
        if self.job.profile.phone is None:
            return ""
        return self.job.profile.phone.replace(" ", "")

    @cached_property
    def candidate_telegram_chat_id(self) -> str:
        if self.profile.is_rami:
            return settings.TELEGRAM_REPORTING_CHAT_ID
        return self.profile.telegram_chat_id

    @cached_property
    def sms_message(self) -> str:
        msg = self.message_salutation + "\n\n"
        if self.profile.lang == "de":
            msg += f"Ich habe Ihnen eine E-Mail bezüglich einer Bewerbung als {self.job_title} geschickt. "
            msg += f"Bei Fragen, rufen Sie an: {self.profile.phone}\n\n"
            msg += "Grüsse,\nRami"
        if self.profile.lang == "en":
            msg += f"I have sent you an e-mail regarding an application as a {self.job_title}. "
            msg += f"If you have any questions, please call: {self.profile.phone}\n\n"
            msg += "Regards,\nRami"
        if self.profile.lang == "es":
            msg += f"Les he enviado un correo electrónico en relación con una candidatura como {self.job_title}. "
            msg += f"Si tiene alguna pregunta, llame al: {self.profile.phone}\n\n"
            msg += "Saludos,\nRami"
        return msg

    def send_sms(self, sms_sender: SMSSender) -> None:
        sms_sender.send_message(self.recruiter_phone, self.sms_message)
        self.sms_sent = True
        self.sms_sent_on = timezone.now()
        self.save()

    def send_email(self) -> None:
        message = EmailMessage(
            subject=self.email_subject,
            body=self.email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[self.job.recruiter.email],
            cc=None if self.profile.is_rami else [self.profile.email],
            reply_to=None if self.profile.is_rami else [self.profile.email],
        )
        message.attach_file(self.local_dossier_path)

        if self.profile.local_docs_path:
            message.attach_file(self.profile.local_docs_path)

        message.send(fail_silently=True)
        self.email_sent = True
        self.email_sent_on = timezone.now()
        self.save()

    def render_dossier(self) -> None:
        # dossier
        self.dossier.delete(save=False)
        template = "jobs/dossier.tex"
        context = {"application": self}
        dossierbytes = latex_render_pdf(template, context, interpreter="pdflatex")
        self.dossier = File(io.BytesIO(dossierbytes), name=self.dossier_filename)
        self.save()
        # check if the page of hiring reasons is included
        page_num = 2 if self.hiringreason_set.count() == 0 else 3
        # letter
        self.cv.delete(save=False)
        self.letter.delete(save=False)
        pages = PdfReader(self.local_dossier_path).pages
        local_letter_path = self.local_dossier_path.parent / self.letter_filename
        letter = PdfWriter(local_letter_path)
        letter.addpages(pages[:page_num])
        letter.write()
        with open(local_letter_path, "rb") as fp:
            self.letter = File(io.BytesIO(fp.read()), name=self.letter_filename)
        # cv
        local_cv_path = self.local_dossier_path.parent / self.cv_filename
        cv = PdfWriter(local_cv_path)
        cv.addpages(pages[page_num:])
        cv.write()
        with open(local_cv_path, "rb") as fp:
            self.cv = File(io.BytesIO(fp.read()), name=self.cv_filename)
        self.save()

    def save(self, *args, **kwargs) -> None:
        if self.email_body is None or self.email_body == "":
            self.email_body = self.get_email_body()
        if self.email_subject is None or self.email_subject == "":
            self.email_subject = self.get_email_subject()

        super().save(*args, **kwargs)
