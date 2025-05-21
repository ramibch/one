import deepl
from django.conf import settings

from one.bot import Bot


def rename_deepl_source(lang: str) -> str:
    """
    Rename the source language according to DeepL API expectations

    https://developers.deepl.com/docs/resources/supported-languages#source-languages

    """
    return lang.upper()


def rename_deepl_target(lang: str) -> str:
    """
    Rename the target language according to DeepL API expectations

    https://developers.deepl.com/docs/resources/supported-languages#target-languages

    """

    adjustments = {"en": "en-gb", "pt": "pt-pt", "zh": "zh-hans"}
    try:
        out = adjustments[lang]
    except KeyError:
        out = lang
    return out.upper()


def translate_text(
    from_lang: str,
    to_lang: str,
    text: str,
    output_if_error: str | None = None,
) -> str | None:
    """
    Translate text with DeepL API
    """
    try:
        return deepl.Translator(settings.DEEPL_AUTH_KEY).translate_text(
            text=text,
            source_lang=rename_deepl_source(from_lang),
            target_lang=rename_deepl_target(to_lang),
        )
    except Exception as e:
        Bot.to_admin(
            f"Failed to translate from {from_lang} to {to_lang}:\n\n'{text}'\n\n"
            f"Exception:\n{e}\n\nReturning: {output_if_error}"
        )
        return output_if_error
