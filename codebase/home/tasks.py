import random

from huey import crontab
from huey.contrib import djhuey as huey

from .models import HomePage


@huey.db_periodic_task(crontab(hour="2", minute="5"))
def change_homepage_sections_daily():
    homepages = HomePage.objects.filter(enable_hero_testing=True, hero__is_active=False).distinct()

    for homepage in homepages:
        active_hero = homepage.hero_set.filter(is_active=True)
        new_active_hero = random.choice(homepage.hero_set.filter(is_active=False))
        active_hero.update(is_active=False)
        new_active_hero.active = True
        new_active_hero.save()
