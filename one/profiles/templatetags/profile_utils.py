from django import template

from tex.models import Tex

register = template.Library()


@register.simple_tag
def allow_cv_creation(request, tex: Tex):
    # TODO: improve this code or remove!
    if tex.is_premium:
        if request.user.is_authenticated:
            return request.user.plan.premium_templates
        else:
            return False

    else:  # if the tex template is not premium anyone can download it
        return True
