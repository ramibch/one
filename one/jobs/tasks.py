from django.db.models import QuerySet
from django.utils import timezone
from huey import crontab
from huey.contrib import djhuey as huey

from one.base.utils.telegram import Bot
from one.candidates.models import Profile

from .models import Application, Job

RAMI_CREATED_A_DOSSIERT_FOR_YOU = {
    "de": "Rami hat eine Bewerbungsmappe für Dich erstellt",
    "en": "Rami has created an application dossier for you.",
    "es": "Rami ha creado un dossier para ti.",
}


def job_apply(applications: QuerySet[Application], per_email: bool = False):
    if not per_email or applications.count() == 0:
        return

    log = "Sending applications\n\n"

    for a in applications:
        log += f"{a.title}\n{a.full_admin_url}\n"
        try:
            if per_email and a.allow_to_send_email:
                a.send_email()
                log += "📧 Email sent\n"
            elif per_email and not a.allow_to_send_email:
                log += "Not allowed to send Email\n"

        except Exception as e:
            log += f"🔴 Error: {e}\n"

        log += "\n"

    Bot.to_admin(log)


def render_dossiers(applications: QuerySet[Application]):
    if applications.count() == 0:
        return

    log = "Rendering dossiers\n\n"

    for a in applications:
        try:
            a.render_dossier()
            log += f"{a.title} | {a.full_admin_url}\n"
            log += f"✅ Dossier rendered: {a.dossier.url}"

            # TODO: Inform user

        except Exception as e:
            log += f"🔴 Error with dossier:\n{e}"

    Bot.to_admin(log)


@huey.task()
def render_dossiers_task(ids):
    qs = Application.objects.filter(id__in=ids)
    render_dossiers(qs)


@huey.task()
def send_jobapps_per_email_task(ids: tuple):
    job_apply(Application.objects.filter(id__in=ids), per_email=True)


## Periodic tasks


@huey.db_periodic_task(crontab(minute="50"))
def render_dossiers_periodic_task():
    qs = Application.objects.filter(dossier__in=("", None))
    render_dossiers(qs)


@huey.db_periodic_task(crontab(minute="55"))
def send_job_applications_per_email():
    applications = Application.objects.filter(
        draft=False,
        email_sent=False,
        job__company__email_allowed=True,
        job__recruiter__email__isnull=False,
    ).exclude(dossier__in=("", None))[:10]

    job_apply(applications, per_email=True)


@huey.db_periodic_task(crontab(minute="59"))
def send_job_applications_per_sms():
    applications = Application.objects.filter(email_sent=True, sms_sent=False).exclude(
        dossier__in=("", None)
    )
    applications = applications.filter(
        email_send_on__gte=timezone.now() - timezone.timedelta(days=2)
    )
    job_apply(applications)


@huey.db_periodic_task(crontab(hour="5", minute="44"))
def recommend_jobs_per_email_periodic_task():
    for profile in Profile.objects.filter(is_rami=False):
        jobs = Job.objects.filter(
            created_on__gt=timezone.now() - timezone.timedelta(days=1),
            position=profile.position,
            location__in=profile.locations.all(),
            lang=profile.lang,
        ).distinct()
        for job in jobs:
            job.recommend_to_profile(profile)


@huey.db_periodic_task(crontab(day_of_week="1,2,3,4,5", hour="8", minute="35"))
def inform_candidate_to_track_app_periodict_task():
    applications = Application.objects.filter(
        email_sent_on__lt=timezone.now() - timezone.timedelta(days=1),
        email_sent_on__gt=timezone.now() - timezone.timedelta(days=7),
        candidate_informed=False,
    )
    if applications.count() == 0:
        return

    for job_app in applications:
        reporting = f"{job_app.job_title_and_id}\n"

        if job_app.job.url:
            reporting += f"{job_app.job.url}\n"

        if job_app.profile.lang == "de":
            reporting += "Empfehlung: Kontaktiere die Firma.\n"

        elif job_app.profile.lang == "en":
            reporting += "Recommendation: Contact the company.\n"

        elif job_app.profile.lang == "es":
            reporting += "Recomendación: Contactar con la empresa.\n"

        reporting += f"🕐 {job_app.email_sent_on}\n"
        reporting += f"🏢 {job_app.job.company.name}\n"
        reporting += f"📍 {job_app.job.company.address}\n"
        if job_app.job.recruiter.email:
            reporting += f"📧 {job_app.job.recruiter.email}\n"
        if job_app.recruiter_phone != "":
            reporting += f"📞 {job_app.recruiter_phone}\n"

        try:
            send_text_to_chat(job_app.candidate_telegram_chat_id, reporting)
        except Exception as e:
            msg = f"Error informing candidate {job_app.full_admin_url}\n{e}"
            Bot.to_admin(msg)
            continue

        job_app.candidate_informed = True
        job_app.save()
