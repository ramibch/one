from django.conf import settings
from django.core.management import call_command
from huey import crontab
from huey.contrib import djhuey as huey


@huey.db_periodic_task(crontab(hour="0", minute="30"))
def django_commands_dairly():
    """
    Typical django commands to run dairly

    """
    call_command("compilemessages", ignore=["venv"], locale=settings.LANGUAGE_CODES_WITHOUT_DEFAULT)
