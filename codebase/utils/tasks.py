from django.conf import settings
from django.db.models import QuerySet
from huey.contrib import djhuey as huey  # type: ignore

from .telegram import Bot
from .translation import translate_text


@huey.task()
def translate_modeltranslation_objects(
    queryset: QuerySet,
    translation_fields: list[str],
):
    from_lang = settings.LANGUAGE_CODE
    out = "🈂️ Translating a multilanguage queryset:\n\n"
    for db_obj in queryset:
        out += f"Object {str(db_obj)}\n"
        if not getattr(db_obj, "allow_translation", False):
            out += "⚠️ Object not allowed to translate. Check: allow_translation.\n\n"
            continue

        for translation_field in translation_fields:
            from_field = f"{translation_field}_{from_lang}"
            from_field_value = getattr(db_obj, from_field)
            if from_field_value is None:
                out += f"Not translating the field {from_field} since it is null.\n"
                continue

            out += f"{from_lang}: {from_field_value}\n"
            for to_lang in settings.LANGUAGE_CODES_WITHOUT_DEFAULT:
                to_field = f"{translation_field}_{to_lang}"
                if getattr(db_obj, to_field) or db_obj.override_translated_fields:
                    continue
                to_field_value = translate_text(from_lang, to_lang, from_field_value)
                setattr(db_obj, to_field, to_field_value)
                out += f"{to_lang}: {to_field_value}\n"
        db_obj.save()
        out += "\n"

    Bot.to_admin(out)
