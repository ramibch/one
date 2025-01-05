import markdown as md
from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.utils.html import format_html

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    return format_html(
        md.markdown(
            value,
            extensions=settings.MARKDOWN_EXTENSIONS,
            extension_configs=settings.MARKDOWN_EXTENSION_CONFIGS,
        )
    )
