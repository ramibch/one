from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand

from ....links.models import Link
from ...models import FooterLink, NavbarLink


def add_navbar_links(link_list: list, show_type: str, start_order: int):
    """Utility function to get a list of NavbarLink objects"""
    new_links = []
    for index, link in enumerate(link_list, start=start_order):
        new_links.append(NavbarLink(link=link, show_type=show_type, order=index))
    return new_links


def add_footer_links(link_list: list):
    """Utility function to get a list of FooterLink objects"""
    new_links = []
    for index, link in enumerate(link_list, start=1):
        new_links.append(FooterLink(link=link, order=index))
    return new_links


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
        link_home = Link.objects.get_or_create(django_url_path="home")[0]

        always_links = (link_search, link_articles, link_plans)
        no_user_links = (link_login, link_logout)
        user_links = (link_dashboard,)

        # Navbar links
        navbar_links = add_navbar_links(always_links, "always", 1)
        navbar_links += add_navbar_links(no_user_links, "no_user", 4)
        navbar_links += add_navbar_links(user_links, "user", 6)
        objs = NavbarLink.objects.bulk_create(
            navbar_links, update_conflicts=True, unique_fields=["link"], update_fields=["link", "order"]
        )
        for obj in objs:
            obj.sites.set(sites)

        # Footer links
        footer_links = add_footer_links([link_home, link_articles, link_search])
        objs = FooterLink.objects.bulk_create(
            footer_links, update_conflicts=True, unique_fields=["link"], update_fields=["link", "order"]
        )
        for obj in objs:
            obj.sites.set(sites)

        self.stdout.write(self.style.SUCCESS("Menus successfully created"))
