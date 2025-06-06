from django.utils.translation import get_language
from jinja2 import Environment

from .filters import FILTERS
from .values import TEX_LANGUAGE_MAPPING


def environment(**options):
    """This code is a copy from https://github.com/weinbusch/django-tex"""

    options.update(
        {
            "autoescape": None,
            "extensions": ["one.tex.extensions.GraphicspathExtension"],
        }
    )
    env = Environment(**options)
    env.filters = FILTERS
    lang = get_language()
    env.globals["tex_lang"] = TEX_LANGUAGE_MAPPING.get(lang) or "english"
    return env
