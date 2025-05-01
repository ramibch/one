from datetime import timedelta
from io import StringIO

import yaml
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import connection
from django.db.models import Q, QuerySet
from django.utils import timezone
from huey import crontab
from huey.contrib import djhuey as huey
from huey.signals import SIGNAL_CANCELED, SIGNAL_ERROR, SIGNAL_LOCKED, SIGNAL_REVOKED
from huey_monitor.models import TaskModel

from .models import SearchTerm
from .utils.abstracts import BaseSubmoduleFolder, TranslatableModel
from .utils.telegram import Bot
from .utils.translation import translate_text

User = get_user_model()


@huey.signal(SIGNAL_ERROR, SIGNAL_LOCKED, SIGNAL_CANCELED, SIGNAL_REVOKED)
def task_not_executed_handler(signal, task, exc=None):
    # This handler will be called for the 4 signals listed, which
    # correspond to error conditions.

    yaml_task = yaml.dump(task, default_flow_style=False)
    msg = f"⚠️ Task not executed ({signal})\n\n{yaml_task}"
    if exc:
        msg += f"\nException: {exc}"
    Bot.to_admin(msg)


@huey.db_periodic_task(crontab(hour="0", minute="0"))
def run_commands_daily():
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
    call_command("clearsessions", stdout=out, stderr=err)
    # call_command("update_rates", verbosity=0, stdout=out, stderr=err)
    # TODO: first install djmoney
    Bot.to_admin(f"Commands\n\nstdout=\n{out.getvalue()}\n\nstderr:{err.getvalue()}\n")


@huey.db_periodic_task(crontab(day_of_week="1", hour="3", minute="2"))
def run_commands_weekly():
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


@huey.db_task()
def translate_modeltranslation_objects(
    queryset: QuerySet[TranslatableModel],
    fields: list[str],
):
    log = "🈂️ Translating a multilanguage queryset:\n\n"
    for db_obj in queryset:
        log += f"Object {str(db_obj)}\n"
        count = 0

        for field in fields:
            from_lang: str = db_obj.get_default_language()
            from_field: str = f"{field}_{from_lang}"
            from_value = getattr(db_obj, from_field)
            if from_value is None or not isinstance(from_value, str):
                log += f"No translation for '{from_field}': null or not a string.\n"
                continue

            log += f"{from_lang}: {from_value}\n"
            for to_lang in db_obj.get_languages_without_default():
                to_field = f"{field}_{to_lang}"
                if (
                    hasattr(db_obj, to_field)
                    and to_lang != from_lang
                    and getattr(db_obj, to_field, None) is None
                ):
                    to_value = translate_text(
                        from_lang=from_lang,
                        to_lang=to_lang,
                        text=from_value,
                    )
                    setattr(db_obj, to_field, to_value)
                    log += f"{to_lang}: {to_value}\n"
                    count += 1

        log += "\n\n"

        if count > 0:
            db_obj.save()

    Bot.to_admin(log)


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


@huey.db_task()
def save_search_query(params):
    SearchTerm.objects.create(**params)


@huey.db_periodic_task(crontab(hour="3", minute="23"))
def remove_db_huey_monitor_task_results():
    """
    Task to remove old task results saved in db.

    Keep the task db objects which have error for debugging.

    """
    past = timezone.now() - timedelta(days=3)
    TaskModel.objects.filter(
        Q(create_dt__lte=past)
        | Q(name="task_send_email_templates")
        | Q(name="task_send_periodic_email_templates_and_reply_messages")
    ).exclude(name=SIGNAL_ERROR).delete()


@huey.periodic_task(crontab(day_of_week="6", hour="14", minute="00"))
def inform_to_admin_about_db_table_sizes():
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT relname AS table_name,
                pg_size_pretty(pg_total_relation_size(c.oid)) AS size_pretty
            FROM pg_class c
            JOIN pg_namespace n ON n.oid = c.relnamespace
            WHERE n.nspname = 'public'
            AND c.relkind = 'r'
            ORDER BY pg_total_relation_size(c.oid) DESC;
        """
        )
        results = cursor.fetchall()

    text = "DB table sizes\n\n"

    for table_name, size_pretty in results:
        text += f"{size_pretty}\t{table_name}\n"

    Bot.to_admin(text)
