from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Creates initial sites that are defined in the setting INITIAL_SITES"

    def add_arguments(self, parser):
        parser.add_argument("--delete-example", action="store_true", help="Remove previously the site example.com")
        parser.add_argument("--delete-all", action="store_true", help="Remove previously all the sites")

    def handle(self, *args, **options):
        if options["delete_example"]:
            Site.objects.filter(domain="example.com").delete()

        if options["delete_all"]:
            Site.objects.all().delete()

        existing_sites = Site.objects.all()
        if existing_sites.count() > 0:
            site_list_as_str = "\n".join([site.domain for site in existing_sites])
            raise CommandError(f"Sites are already created.\n{site_list_as_str}")

        initial_sites = getattr(settings, "INITIAL_SITES", None)

        if initial_sites is None:
            raise CommandError("The setting INITIAL_SITES is not defined.")

        created_sites = []

        for site_name, site_domain in initial_sites:
            created_sites.append(Site.objects.create(name=site_name, domain=site_domain))

        created_sites_as_str = "\n".join([site.domain for site in created_sites])
        self.stdout.write(self.style.SUCCESS(f"Sites successfully created:\n{created_sites_as_str}"))
