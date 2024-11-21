import random

from huey import crontab
from huey.contrib import djhuey as huey

from .models import HomePage


@huey.db_periodic_task(crontab(hour="2", minute="5"))
def change_homepagehero_sections_daily():
    homepages = HomePage.objects.filter(enable_section_changing=True).distinct()

    for home in homepages:
        # Hero
        new_hero = random.choice(home.homehero_set.filter(is_active=False))
        new_hero.is_active = True
        new_hero.save()
