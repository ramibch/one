import subprocess
from io import StringIO

from django.conf import settings
from django.core.management import call_command
from django.db.models import Model, QuerySet
from huey import crontab
from huey.contrib import djhuey as huey

from codebase.sites.models import Site

from .utils.abstracts import BaseSubmodule
from .utils.telegram import Bot
from .utils.translation import translate_text


@huey.db_periodic_task(crontab(hour="0", minute="0"))
def django_commands_daily():
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
    call_command("update_rates", verbosity=0, stdout=out, stderr=err)
    Bot.to_admin(
        f"Django commands\n\nstdout=\n{out.getvalue()}\n\nstderr:{err.getvalue()}\n"
    )


@huey.db_periodic_task(crontab(hour="0", minute="10"))
def fetch_submodules_daily():
    ok = subprocess.call(["git", "submodule", "update", "--remote"]) == 0
    emoji_ok = "✅" if ok else "🔴"
    Bot.to_admin(f"{emoji_ok} Submodules fetched")


@huey.db_periodic_task(crontab(hour="0", minute="15"))
def check_sites_without_home_daily():
    sites = Site.objects.filter(homepage__isnull=True)
    if sites.count() == 0:
        return
    sites_str = "\n".join(site.domain for site in sites)
    Bot.to_admin(f"⚠️ These sites have no Home associated:\n\n{sites_str}")


@huey.db_periodic_task(crontab(hour="0", minute="16"))
def check_sites_without_userhome_daily():
    sites = Site.objects.filter(userhomepage__isnull=True)
    if sites.count() == 0:
        return
    sites_str = "\n".join(site.domain for site in sites)
    Bot.to_admin(f"⚠️ These sites have no UserHome associated:\n\n{sites_str}")


@huey.db_periodic_task(crontab(hour="0", minute="20"))
def sync_submodule_folders_every_1_hour(hour="/*"):
    """Syncs all submodule folders"""

    BaseSubmodule.sync_all_folders()


@huey.task()
def translate_modeltranslation_objects(
    queryset: QuerySet[type[Model]],
    translation_fields: list[str],
):
    out = "🈂️ Translating a multilanguage queryset:\n\n"
    for db_obj in queryset:
        out += f"Object {str(db_obj)}\n"
        if not hasattr(db_obj, "allow_translation"):
            out += "⚠️ Object not allowed to translate. Check: allow_translation.\n\n"
            continue

        for translation_field in translation_fields:
            from_field = f"{translation_field}_{db_obj.get_default_language().id}"
            from_field_value = getattr(db_obj, from_field)
            if from_field_value is None:
                out += f"Not translating the field {from_field} since it is null.\n"
                continue

            out += f"{db_obj.default_language}: {from_field_value}\n"
            for to_language in db_obj.get_rest_languages():
                to_field = f"{translation_field}_{to_language.id}"
                if (
                    not hasattr(db_obj, to_field)
                    or not db_obj.override_translated_fields
                    or to_language.id == db_obj.default_language.id
                ):
                    continue
                to_field_value = translate_text(
                    from_language=db_obj.default_language.id,
                    to_lang=to_language.id,
                    text=from_field_value,
                )
                setattr(db_obj, to_field, to_field_value)
                out += f"{to_language}: {to_field_value}\n"
        db_obj.save()
        out += "\n\n"

    Bot.to_admin(out)
