import deepl
from django.conf import settings

from .telegram import Bot


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


def translate_text(from_lang: str, to_lang: str, text: str) -> str | None:
    """
    Translate text with DeepL API
    """

    translator = deepl.Translator(settings.DEEPL_AUTH_KEY)

    try:
        return translator.translate_text(
            text=text,
            source_lang=rename_deepl_source(from_lang),
            target_lang=rename_deepl_target(to_lang),
        )
    except Exception as e:
        Bot.to_admin(f"Failed to translate this text from {from_lang} to {to_lang}:{text}\nException:\n{e}")
