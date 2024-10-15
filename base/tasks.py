from io import StringIO

from django.conf import settings
from django.core.management import call_command
from huey import crontab
from huey.contrib import djhuey as huey

from .telegram import Bot


@huey.db_periodic_task(crontab(hour="0", minute="30"))
def django_commands_dairly():
    """
    Typical django commands to run dairly

    """
    out, err = StringIO(), StringIO()

    call_command("compilemessages", ignore=["venv"], locale=settings.LANGUAGE_CODES_WITHOUT_DEFAULT, stdout=out, stderr=err)

    call_command("check", deploy=True, stdout=out, stderr=err)

    Bot.to_admin(f"Django commands\n\nstdout=\n{out.getvalue()}\n\stderr:{err.getvalue()}\n")
