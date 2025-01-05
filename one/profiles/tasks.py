from datetime import datetime, timedelta

from django.utils import translation
from django.utils.translation import gettext as _
from huey import crontab
from huey.contrib.djhuey import db_periodic_task
from utils.email import send_simple_email
from utils.telegram import report_to_admin

from .models import Profile


@db_periodic_task(crontab(hour="8", minute="10"))
def notify_to_complete_profile():
    # Get last updated profiles
    profiles = Profile.objects.filter(
        email__isnull=False,
        category__in=("temporal", "user_profile"),
        updated__gt=datetime.now() - timedelta(days=1),
    )
    # Collect emails depending on the profile completion
    profiles_to_email = []
    for p in profiles:
        if not p.has_children_exclude("cv_set"):
            profiles_to_email.append(p)

    # Send emails
    # p = profiles_to_email[0]  # GoDaddy limits :(
    for profile in profiles_to_email:
        with translation.override(profile.language):
            subject = "Nice CV | " + _("Complete your profile")
            body = _("Hello x")
            if p.fullname is not None:
                body += " " + p.fullname
            body += ",\n\n"
            body += _("This is Rami from nicecv.online.")
            body += "\n\n"
            body += _("I am glad you want to improve the aesthetics of your CV.")
            body += "\n\n"
            body += _(
                "I writing to you because it seems that you decided to abandon the process of creating a CV that will impress recruiters."
            )
            body += " "
            body += _(
                "But if you want to complete your profile and download CV templates, visit the site:"
            )
            body += "\n\n"
            body += "https://nicecv.online"
            body += "\n\n"
            body += _("Best wishes, Rami.")

            send_simple_email(subject=subject, body=body, to=p.email)


@db_periodic_task(crontab(hour="0", minute="15"))
def remove_temporal_profiles():
    # Delete recent temporal profiles with no fullname and no email
    recent_profiles = Profile.objects.filter(
        category="temporal",
        updated__lt=datetime.now() - timedelta(days=1),
        fullname__isnull=True,
        email__isnull=True,
    )
    report_to_admin(f"Deleted {recent_profiles.count()} recent temporal profiles")
    recent_profiles.delete()
