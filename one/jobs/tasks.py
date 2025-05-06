from django.utils import timezone
from huey import crontab
from huey.contrib import djhuey as huey

from .models import Job


@huey.db_periodic_task(crontab(hour="3", minute="12"))
def update_job_status_daily_task():
    now = timezone.now()
    active_jobs = Job.objects.filter(is_active=True)
    pk_list = [job.pk for job in active_jobs if job.expires_on < now]
    Job.objects.filter(pk__in=pk_list).update(is_active=False)
