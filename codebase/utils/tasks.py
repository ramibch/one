from django.conf import settings
from huey.contrib import djhuey as huey


def dummy_translate(from_lang, to_lang, text):
    # TODO: implement DeepL API
    return f"Dummy translation: {from_lang} -> {to_lang}."


@huey.task()
def translate_null_field_from_a_queryset(queryset, translation_fields):
    for db_obj in queryset:
        for field in translation_fields:
            from_field = f"{field}_{settings.LANGUAGE_CODE}"
            from_field_value = getattr(db_obj, from_field)
            if from_field_value is None:
                continue

            for to_lang in settings.LANGUAGE_CODES_WITHOUT_DEFAULT:
                to_field = f"{field}_{to_lang}"
                if getattr(db_obj, to_field) is not None:
                    continue
                setattr(db_obj, to_field, dummy_translate(settings.LANGUAGE_CODE, to_lang, from_field_value))
        db_obj.save()
