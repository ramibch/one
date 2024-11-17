from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError

from ...models import ExtendedSite


class Command(BaseCommand):
    help = "Creates initial sites that are defined in the setting SITES"

    def add_arguments(self, parser):
        parser.add_argument("environments", nargs="+", type=str)
        parser.add_argument("--delete-example", action="store_true", help="Remove previously the site example.com")
        parser.add_argument("--delete-all", action="store_true", help="Remove previously all the sites")

    def handle(self, *args, **options):
        if options["delete_example"]:
            Site.objects.filter(domain="example.com").delete()

        if options["delete_all"]:
            Site.objects.all().delete()

        sites = getattr(settings, "SITES", None)

        if sites is None:
            raise CommandError("The setting SITES is not defined.")

        created_sites = []

        for env in options["environments"]:
            try:
                env_sites = sites[env]
            except KeyError:
                raise CommandError(f"Environment {env} unrecognised in SITES.")  # noqa: B904

            for site_name, site_domain in env_sites:
                extsite, created = ExtendedSite.objects.get_or_create(name=site_name, domain=site_domain)
                if created:
                    created_sites.append(extsite)
        if len(created_sites) > 0:
            created_sites_as_str = "\n".join([site.domain for site in created_sites])
            self.stdout.write(self.style.SUCCESS(f"Sites for '{env}' successfully created:\n{created_sites_as_str}"))
        else:
            self.stdout.write(self.style.WARNING(f"Sites for '{env}' are already created"))
