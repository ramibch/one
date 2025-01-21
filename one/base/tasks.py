from io import StringIO

from django.conf import settings
from django.core.management import call_command
from django.db.models import Model, QuerySet
from huey import crontab
from huey.contrib import djhuey as huey
from huey.signals import SIGNAL_CANCELED, SIGNAL_ERROR, SIGNAL_LOCKED, SIGNAL_REVOKED

from .utils.abstracts import BaseSubmoduleFolder
from .utils.telegram import Bot
from .utils.translation import translate_text


@huey.signal()
def all_signal_handler(signal, task, exc=None):
    # This handler will be called for every signal.
    Bot.to_admin(f"{signal} - {task.id}")


@huey.signal(SIGNAL_ERROR, SIGNAL_LOCKED, SIGNAL_CANCELED, SIGNAL_REVOKED)
def task_not_executed_handler(signal, task, exc=None):
    # This handler will be called for the 4 signals listed, which
    # correspond to error conditions.
    Bot.to_admin(f"[{signal}] {task.id} - not executed")


@huey.db_periodic_task(crontab(hour="0", minute="0"))
def commands_daily():
    """
    Typical django commands to run daily

    """
    out, err = StringIO(), StringIO()
    call_command(
        "compilemessages",
        ignore=[".venv", "venv"],
        locale=settings.LANGUAGE_CODES_WITHOUT_DEFAULT,
        stdout=out,
        stderr=err,
    )
    call_command("check", deploy=True, stdout=out, stderr=err)
    call_command("clearsessions", deploy=True, stdout=out, stderr=err)
    call_command("update_rates", verbosity=0, stdout=out, stderr=err)
    Bot.to_admin(f"Commands\n\nstdout=\n{out.getvalue()}\n\nstderr:{err.getvalue()}\n")


@huey.db_periodic_task(crontab(hour="0", minute="0"))
def commands_weekly():
    """
    Some commands to run weekly
    """
    out, err = StringIO(), StringIO()
    call_command("dbbackup", verbosity=0, stdout=out, stderr=err)
    Bot.to_admin(
        f"Weekly commands\n\nstdout=\n{out.getvalue()}\n\nstderr:{err.getvalue()}\n"
    )


@huey.db_periodic_task(crontab(hour="0", minute="20"))
def sync_submodule_folders_task():
    """Syncs all submodule folders"""

    BaseSubmoduleFolder.sync_folders()


@huey.task()
def translate_modeltranslation_objects(
    queryset: QuerySet[type[Model]],
    fields: list[str],
):
    out = "🈂️ Translating a multilanguage queryset:\n\n"
    for db_obj in queryset:
        out += f"Object {str(db_obj)}\n"
        if not hasattr(db_obj, "allow_translation"):
            out += "⚠️ Object not allowed to translate. Check: allow_translation.\n\n"
            continue

        for field in fields:
            from_field = f"{field}_{db_obj.get_default_language()}"
            from_field_value = getattr(db_obj, from_field)
            if from_field_value is None:
                out += f"Not translating the field {from_field} since it is null.\n"
                continue

            out += f"{db_obj.get_default_language()}: {from_field_value}\n"
            for to_language in db_obj.get_rest_language():
                to_field = f"{field}_{to_language}"
                if (
                    hasattr(db_obj, to_field)
                    and db_obj.override_translated_fields
                    and to_language != db_obj.get_default_language()
                ):
                    to_field_value = translate_text(
                        from_language=db_obj.get_default_language(),
                        to_lang=to_language,
                        text=from_field_value,
                    )
                    setattr(db_obj, to_field, to_field_value)
                    out += f"{to_language}: {to_field_value}\n"
        db_obj.save()
        out += "\n\n"

    Bot.to_admin(out)


@huey.db_periodic_task(crontab(minute="21"))
def settings_check_task_hourly():
    """
    Checks the settings
    """

    msg = ""

    if settings.ENV != "prod":
        msg += "⚠️ ENV is not 'prod'\n\n"

    if settings.DEBUG:
        msg += "⚠️ DEBUG is True\n\n"

    if not settings.HTTPS:
        msg += "⚠️ HTTPS is False\n\n"

    if msg != "":
        Bot.to_admin(f"Settings checker:\n\n{msg}")
