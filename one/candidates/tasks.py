from django.db.models import F, Q
from huey import crontab
from huey.contrib import djhuey as huey

from .models import Candidate, JobApplication, TexCv, TexCvTemplates


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
