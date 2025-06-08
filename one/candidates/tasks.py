from huey import crontab
from huey.contrib import djhuey as huey

from .models import JobApplication, TexCv


@huey.db_periodic_task(crontab(minute="*"))
def task_render_cvs(cv_objs=None):
    if cv_objs is None:
        cv_objs = TexCv.objects.filter(cv_pdf__in=["", None])

    for cv_obj in cv_objs:
        cv_obj.render_cv()


@huey.db_periodic_task(crontab(minute="*"))
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
