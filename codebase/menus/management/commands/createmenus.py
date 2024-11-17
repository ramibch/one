from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand

from ....links.models import Link
from ...models import NavbarLink


class Command(BaseCommand):
    help = "Creates initial menus"

    def handle(self, *args, **options):
        sites = Site.objects.all()

        link_search = Link.objects.get_or_create(django_url_path="search")[0]
        link_articles = Link.objects.get_or_create(django_url_path="article_list")[0]
        link_plans = Link.objects.get_or_create(django_url_path="plan_list")[0]
        link_login = Link.objects.get_or_create(django_url_path="account_login")[0]
        link_logout = Link.objects.get_or_create(django_url_path="account_signup")[0]
        link_dashboard = Link.objects.get_or_create(django_url_path="user_dashboard")[0]

        always_links = (link_search, link_articles, link_plans)
        nouser_links = (link_login, link_logout)
        user_links = (link_dashboard,)

        navbar_links = []
        for index, link in enumerate(always_links, start=1):
            navbar_links.append(NavbarLink(link=link, show_type="always", order=index))

        for index, link in enumerate(nouser_links, start=4):
            navbar_links.append(NavbarLink(link=link, show_type="no_user", order=index))

        for index, link in enumerate(user_links, start=6):
            navbar_links.append(NavbarLink(link=link, show_type="user", order=index))

        for navbarlink in NavbarLink.objects.bulk_create(navbar_links):
            navbarlink.sites.set(sites)

        # update_conflicts=True, update_fields=("link", "show_type", "")

        self.stdout.write(self.style.SUCCESS("Menus successfully created"))
