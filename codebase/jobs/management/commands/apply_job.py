import random

from django.core.management.base import BaseCommand

from jobs.models import RockenJobApplication
from utils.telegram import report_to_admin


class Command(BaseCommand):
    help = "Publish a random social post that has not been published yet."

    def handle(self, *args, **options):
        self.stdout.write("Applying...")
        applications = RockenJobApplication.objects.filter(applied=False)
        if applications.count() > 0:
            application = random.choice(list(applications))
            application.apply()
            self.stdout.write("Applied.")
            report_to_admin(
                f"Applied to {application.job.vacancy_url} for {application.profile.first_name}"
            )
        else:
            self.stdout.write("No applications found...")
