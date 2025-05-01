# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from utils.telegram import report_to_admin

from .models import Application, Job, Profile


def apply_per_email(request, profile_id, job_id):
    email = request.GET.get("email", None)

    if email is None:
        return HttpResponse(status=400)

    profile = get_object_or_404(Profile, email=email, id=profile_id)
    job = get_object_or_404(Job, id=job_id)

    try:
        Application.objects.create(profile=profile, job=job)
    except Exception:
        return HttpResponse(_("You already applied to this job."))

    # report to admin
    try:
        reporting = f"{profile.fullname} ({profile.email}) applied to job {job.title}"
        report_to_admin(reporting)
    except Exception:
        pass

    return HttpResponse(_("Great! I will apply shortly to this job for you."))


def delete_profile(request, id):
    email = request.GET.get("email", None)
    profile = get_object_or_404(Profile, email=email, id=id)
    try:
        reporting = f"{profile.fullname} ({profile.email}) removed his/her profile"
        report_to_admin(reporting)
    except Exception:
        pass
    profile.delete()
    return HttpResponse(_("Your data has been deleted from my site."))
