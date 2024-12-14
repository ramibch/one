import random

from huey import crontab
from huey.contrib import djhuey as huey

from .models import Home


@huey.db_periodic_task(crontab(hour="2", minute="5"))
def change_homepage_sections_daily():
    homes = Home.objects.filter(enable_section_changing=True).distinct()

    for home in homes:
        active_hero = home.hero_set.filter(is_active=True)
        new_active_hero = random.choice(home.homehero_set.filter(is_active=False))
        active_hero.update(is_active=False)
        new_active_hero.active = True
        new_active_hero.save()
