import subprocess
from io import StringIO

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management import call_command
from huey import crontab
from huey.contrib import djhuey as huey

from ..utils.abstracts import AbstractSubmoduleFolderModel
from ..utils.telegram import Bot


@huey.db_periodic_task(crontab(hour="0", minute="0"))
def django_commands_daily():
    """
    Typical django commands to run daily

    """
    out, err = StringIO(), StringIO()

    call_command("compilemessages", ignore=["venv"], locale=settings.LANGUAGE_CODES_WITHOUT_DEFAULT, stdout=out, stderr=err)

    call_command("check", deploy=True, stdout=out, stderr=err)

    call_command("update_rates", verbosity=0, stdout=out, stderr=err)

    Bot.to_admin(f"Django commands\n\nstdout=\n{out.getvalue()}\n\nstderr:{err.getvalue()}\n")


@huey.db_periodic_task(crontab(hour="0", minute="10"))
def fetch_submodules_daily():
    ok = subprocess.call(["git", "submodule", "update", "--remote"]) == 0

    emoji_ok = "✅" if ok else "🔴"

    Bot.to_admin(f"{emoji_ok} Submodules fetched")


@huey.db_periodic_task(crontab(hour="0", minute="15"))
def check_sites_without_extended_sites_daily():
    sites = Site.objects.filter(extended__isnull=True)

    if sites.count() == 0:
        return

    sites_str = "\n".join(site.domain for site in sites)
    Bot.to_admin(f"⚠️ The following sites have no Site Profile associated:\n\n{sites_str}")


@huey.db_periodic_task(crontab(hour="0", minute="10"))
def sync_submodule_folders_every_1_hour(hour="/*"):
    """Syncs all submodule folders"""

    for SubmoduleFolderModel in AbstractSubmoduleFolderModel.__subclasses__():
        SubmoduleFolderModel.sync_folders()
