from django.db.models import QuerySet
from django.utils import timezone
from huey import crontab
from huey.contrib import djhuey as huey
from utils.telegram import report_to_admin, send_text_to_chat
from utils.webdrivers import SMSSender

from .models import Application, Job, Profile

RAMI_CREATED_A_DOSSIERT_FOR_YOU = {
    "de": "Rami hat eine Bewerbungsmappe für Dich erstellt",
    "en": "Rami has created an application dossier for you.",
    "es": "Rami ha creado un dossier para ti.",
}


def apply(apps: QuerySet[Application], per_email: bool = False, per_sms: bool = False):
    try:
        iter(apps)
    except TypeError:
        return

    if not per_email and not per_sms or apps.count() == 0:
        return

    reporting = "Sending applications\n\n"

    if per_sms:
        sms_sender = SMSSender()

    for app in apps:
        reporting += f"{app.title}\n{app.full_admin_url}\n"
        try:
            if per_email and app.allow_to_send_email:
                app.send_email()
                reporting += "📧 Email sent\n"
            elif per_email and not app.allow_to_send_email:
                reporting += "Not allowed to send Email\n"

            if per_sms and app.allow_to_send_sms_to_recruiter:
                app.send_sms(sms_sender=sms_sender)
                reporting += "💬 SMS sent\n"
            elif per_sms and not app.allow_to_send_sms_to_recruiter:
                reporting += "Not allowed to send SMS\n"
        except Exception as e:
            reporting += f"🔴 Error: {e}\n"

        reporting += "\n"

    if per_sms:
        sms_sender.logout_and_close()

    report_to_admin(reporting)


def render_dossiers(apps: QuerySet[Application]):
    try:
        iter(apps)
    except TypeError:
        return

    if apps.count() == 0:
        return

    reporting = "Rendering dossiers\n\n"

    for job_app in apps:
        try:
            job_app.render_dossier()
            reporting += f"{job_app.title} | {job_app.full_admin_url}\n"
            reporting += f"✅ Dossier rendered: {job_app.dossier.url}"

            if not job_app.profile.is_rami and job_app.profile.telegram_chat_id:
                d = {
                    "de": "Rami hat eine Bewerbungsmappe für Dich erstellt",
                    "en": "Rami has created an application dossier for you.",
                    "es": "Rami ha creado un dossier para ti.",
                }
                user_reporting = f"{d[job_app.profile.lang]}\n{job_app.dossier.url}"
                send_text_to_chat(job_app.profile.telegram_chat_id, user_reporting)

        except Exception as e:
            reporting += f"🔴 Error with dossier:\n{e}"

    report_to_admin(reporting)


@huey.task()
def render_dossiers_task(ids):
    qs = Application.objects.filter(id__in=ids)
    render_dossiers(qs)


@huey.task()
def send_jobapps_per_email_task(ids: tuple):
    apply(Application.objects.filter(id__in=ids), per_email=True)


@huey.task()
def send_jobapps_per_sms_task(ids: tuple):
    apply(Application.objects.filter(id__in=ids), per_sms=True)


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
    apply(applications, per_email=True)


@huey.db_periodic_task(crontab(minute="59"))
def send_job_applications_per_sms():
    applications = Application.objects.filter(email_sent=True, sms_sent=False).exclude(
        dossier__in=("", None)
    )
    applications = applications.filter(
        email_send_on__gte=timezone.now() - timezone.timedelta(days=2)
    )
    apply(applications, per_sms=True)


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

    sms_sender = SMSSender()

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

        if job_app.allow_to_send_sms_to_candidate:
            sms_sender.send_message(job_app.candidate_phone, reporting)

        try:
            send_text_to_chat(job_app.candidate_telegram_chat_id, reporting)
        except Exception as e:
            msg = f"Error informing candidate {job_app.full_admin_url}\n{e}"
            report_to_admin(msg)
            continue

        job_app.candidate_informed = True
        job_app.save()

    sms_sender.logout_and_close()


@huey.db_periodic_task(crontab(minute="26"))
def promote_job_periodic_task():
    job = Job.objects.filter(
        created_on__gt=timezone.now() - timezone.timedelta(days=14),
        url__isnull=False,
        promoted=False,
    ).first()
    if job is not None:
        job.promote()
