from django import template

from ..models import DgtTest, SessionDgtTest

register = template.Library()


@register.simple_tag
def sessiontest_emojis(request, test: DgtTest):
    qs = SessionDgtTest.objects.filter(test=test, session=request.db_session)[:5]
    return "".join(sessiontest.passed_emoji for sessiontest in qs)
