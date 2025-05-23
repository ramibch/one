from django import template

from one.db import get_db_session_object

from ..models import DgtTest, SessionDgtTest

register = template.Library()


@register.simple_tag
def sessiontest_emojis(request, test: DgtTest):
    session = get_db_session_object(request)
    qs = SessionDgtTest.objects.filter(test=test, session=session)[:5]
    return "".join(sessiontest.passed_emoji for sessiontest in qs)
