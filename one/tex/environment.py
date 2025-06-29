from django.utils import translation
from jinja2 import Environment

from .filters import FILTERS


def environment(**options):
    """This code is a copy from https://github.com/weinbusch/django-tex"""

    options.update(
        {
            "autoescape": None,
            "extensions": [
                "jinja2.ext.i18n",
                "one.tex.extensions.GraphicspathExtension",
            ],
        }
    )
    env = Environment(**options)
    env.filters = FILTERS
    # Language not working properly when passing
    # Huey and Django worker?
    # lang = get_language()
    # env.globals["tex_lang"] = TEX_LANGUAGE_MAPPING.get(lang) or "english"
    env.install_gettext_translations(translation)
    return env
