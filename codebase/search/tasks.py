from django.contrib.auth import get_user_model
from huey.contrib import djhuey as huey

from .models import SearchTerm

User = get_user_model()


@huey.task()
def save_search_query(q, cc, u):
    SearchTerm.objects.create(query=q, country_code=cc, user=u)
