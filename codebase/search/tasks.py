from django.contrib.auth import get_user_model
from huey.contrib import djhuey as huey

from .models import SearchTerm

User = get_user_model()


@huey.db_task()
def save_search_query(params):
    SearchTerm.objects.create(**params)
