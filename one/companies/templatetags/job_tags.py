from django import template

from one.candidates.models import JobApplication

register = template.Library()


@register.simple_tag
def has_candidate_applied(candidate, job) -> bool:
    return JobApplication.objects.filter(candidate=candidate, job=job).exists()
