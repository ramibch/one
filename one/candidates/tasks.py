from datetime import timedelta

from django.core.mail import EmailMessage
from django.db.models import F, Q, QuerySet
from django.template.loader import render_to_string
from django.utils import timezone, translation
from django.utils.translation import gettext_lazy as _
from huey import crontab
from huey.contrib import djhuey as huey

from one.bot import Bot
from one.companies.models import JobApplicationMethods
from one.sites.models import Site

from .models import (
    Candidate,
    JobApplication,
    TexCv,
    TexCvTemplates,
    get_email_sender,
)


# Temporary deactivated
# @huey.db_periodic_task(crontab(minute="*"))
def task_create_texcvs(candidates=None):
    if candidates is None:
        candidates = Candidate.objects.filter(texcv__isnull=True)

    cvs = []
    for candidate in candidates:
        cvs.append(TexCv(candidate=candidate, template=TexCvTemplates.ALICE))
        # for cv_template in TexCvTemplates.values:
        # TODO: implement all cv templates (first tex files)
        # cvs.append(TexCv(candidate=candidate, template=cv_template))

    TexCv.objects.bulk_create(cvs, ignore_conflicts=True)


# Temporary deactivated
# @huey.db_periodic_task(crontab(minute="*"))
def task_render_cvs(cv_objs=None):
    if cv_objs is None:
        cv_objs = TexCv.objects.filter(
            Q(cv_pdf__isnull=True)
            | Q(cv_pdf="")
            | Q(updated_at__lt=F("candidate__updated_at"))
            | Q(updated_at__lt=F("candidate__candidateskill__updated_at"))
            | Q(updated_at__lt=F("candidate__candidateexperience__updated_at"))
            | Q(updated_at__lt=F("candidate__candidateeducation__updated_at"))
        ).distinct()
    for cv_obj in cv_objs:
        cv_obj.render_cv()


# Temporary deactivated
# @huey.db_periodic_task(crontab(minute="*"))
def task_render_coverletters(job_apps=None):
    if job_apps is None:
        job_apps = JobApplication.objects.filter(coverletter__in=["", None])

    for job_app in job_apps:
        job_app.render_coverletter()


@huey.db_periodic_task(crontab(minute="*"))
def task_render_dossiers(job_apps=None):
    if job_apps is None:
        job_apps = JobApplication.objects.filter(dossier__in=["", None])

    for job_app in job_apps:
        job_app.render_dossier()


@huey.db_periodic_task(crontab(minute="*"))
def task_send_applications_per_email():
    job_apps = JobApplication.objects.filter(
        sent_on__isnull=True,
        job__company__job_application_methods__contains=[JobApplicationMethods.EMAIL],
    ).exclude(dossier="")

    for job_app in job_apps:
        job_app.send_application_per_email()


@huey.db_periodic_task(crontab(hour="8", minute="7"))
def task_recommend_jobs(candidates: QuerySet[Candidate] | None = None):
    base_filters = {
        "recommend_jobs": True,
        "email__isnull": False,
    }

    if candidates is None:
        candidates = Candidate.objects.all()

    candidates = candidates.filter(**base_filters).filter(
        Q(last_job_recommendation__isnull=True)
        | Q(last_job_recommendation__lt=timezone.now() - timedelta(days=7))
    )

    site: Site = Site.objects.get_jobapps_site()  # type: ignore

    for c in candidates:
        jobs = c.recommended_jobs()
        if jobs.count() == 0:
            continue

        with translation.override(c.language):
            email_body = render_to_string(
                "candidates/emails/recommend_jobs.txt",
                context={"candidate": c, "jobs": jobs[:20], "url": site.url},
                request=None,
            )

            message = EmailMessage(
                subject=_("Recommended jobs for you!"),
                body=email_body,
                from_email=get_email_sender(),
                to=[c.email],
            )

            try:
                message.send(fail_silently=False)
                c.last_job_recommendation = timezone.now()
                c.save(update_fields=["last_job_recommendation"])
            except Exception as e:
                Bot.to_admin(f"Failed to recommend job to canidate {c.id}: {e}")
