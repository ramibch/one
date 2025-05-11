from datetime import timedelta
from http import HTTPStatus
from urllib.parse import urlparse

import langdetect
import requests
from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils import timezone
from huey import crontab
from huey.contrib import djhuey as huey

from one.base.utils.telegram import Bot
from one.companies.models import Company
from one.jobs.models import Job

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) C hrome/102.0.0.0 Safari/537.36"
    )
}


validate_url = URLValidator()


@huey.db_periodic_task(crontab(hour="21", minute="30"))
def generate_jobs():
    log = ""
    jobs = []

    companies = Company.objects.filter(
        jobs_page_url__isnull=False,
        jobs_scrape_ready=True,
    )

    for company in companies:
        response = requests.get(company.jobs_page_url, headers=headers)

        if response.status_code != HTTPStatus.OK:
            log += f"{response.status_code} {company.jobs_page_url}"
            continue

        if company.jobs_page_html == response.text:
            continue

        company.jobs_page_html = response.text

        company.save()

        page_soup = BeautifulSoup(response.content.decode("utf-8"), "html.parser")

        if company.jobs_container_class:
            soup = page_soup.find(
                company.jobs_container_tag, company.jobs_container_class
            )
        else:
            soup = page_soup.find(company.jobs_container_tag)

        if soup is None:
            continue

        if company.job_link_class:
            elements = soup.find_all("a", company.job_link_class, href=True)
        else:
            elements = soup.find_all("a", href=True)

        loc = (
            company.companylocation_set.first()
            if company.companylocation_set.count() == 1
            else None
        )

        language = langdetect.detect(page_soup.text)

        for element in elements:
            href = element.get("href")
            if not href:
                continue
            try:
                validate_url(href)
                url = href
            except ValidationError:
                purl = urlparse(response.url)
                url = f"{purl.scheme}//{purl.netloc}{href}"

            if Job.objects.filter(source_url=url).exists():
                continue

            jobs.append(
                Job(
                    title=element.text[:128],
                    source_url=url,
                    expires_on=timezone.now() + timedelta(days=60),
                    company_location=loc,
                    language=language,
                )
            )

    Job.objects.bulk_create(jobs, ignore_conflicts=True)

    if log:
        Bot.to_admin(log)
