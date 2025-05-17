from datetime import timedelta
from http import HTTPStatus
from urllib.parse import urlparse

import langdetect
import markdownify
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


@huey.db_periodic_task(crontab(hour="3", minute="12"))
def update_job_status_daily_task():
    now = timezone.now()
    active_jobs = Job.objects.filter(is_active=True)
    pk_list = [job.pk for job in active_jobs if job.expires_on < now]
    Job.objects.filter(pk__in=pk_list).update(is_active=False)


validate_url = URLValidator()


@huey.db_periodic_task(crontab(hour="*/4", minute="30"))
def scrape_and_create_jobs():
    log = ""
    companies = Company.objects.filter(
        jobs_page_url__isnull=False,
        jobs_scrape_ready=True,
    )

    for c in companies:
        response = requests.get(c.jobs_page_url, headers=headers)

        if response.status_code != HTTPStatus.OK:
            log += f"{response.status_code} {c.jobs_page_url}\n"
            continue

        if c.jobs_page_html == response.text:
            continue

        c.jobs_page_html = response.text

        c.save()

        page_soup = BeautifulSoup(response.content.decode("utf-8"), "html.parser")

        if c.jobs_container_id and c.jobs_container_class:
            soup = page_soup.find(
                c.jobs_container_tag, c.jobs_container_class, id=c.jobs_container_id
            )
        elif c.jobs_container_class:
            soup = page_soup.find(c.jobs_container_tag, c.jobs_container_class)
        elif c.jobs_container_id:
            soup = page_soup.find(c.jobs_container_tag, id=c.jobs_container_id)
        else:
            soup = page_soup.find(c.jobs_container_tag)

        if soup is None:
            continue

        if c.job_link_class:
            elements = soup.find_all("a", c.job_link_class, href=True)
        else:
            elements = soup.find_all("a", href=True)

        loc = (
            c.companylocation_set.first()
            if c.companylocation_set.count() == 1
            else None
        )

        language = langdetect.detect(page_soup.text)

        for element in elements:
            href = element.get("href")
            if not href:
                continue

            if href.startswith("mailto"):
                continue

            try:
                validate_url(href)
                url = href
            except ValidationError:
                parsed_url = urlparse(response.url)
                href = href if href.startswith("/") else f"/{href}"
                url = f"{parsed_url.scheme}://{parsed_url.netloc}{href}"
                try:
                    validate_url(url)
                except ValidationError:
                    log += f"Error with {url}\n"
                    continue

            if Job.objects.filter(source_url=url).exists():
                continue

            job = Job.objects.create(
                title=element.text[:128],
                source_url=url,
                company=c,
                expires_on=timezone.now() + timedelta(days=60),
                language=language,
            )
            if loc:
                job.company_locations.add(loc)

    if log:
        Bot.to_admin("Generating jobs\n" + log)


@huey.db_periodic_task(crontab(hour="*/4", minute="45"))
def scrape_job_detail_pages_and_update_its_attrs():
    log = ""

    jobs = Job.objects.filter(
        body__isnull=True,
        source_url__isnull=False,
        company__isnull=False,
    )

    for job in jobs:
        response = requests.get(job.source_url, headers=headers)

        if response.status_code != HTTPStatus.OK:
            log += f"{response.status_code} {job.source_url}\n"
            continue

        page_soup = BeautifulSoup(response.content.decode("utf-8"), "html.parser")

        container_tag = job.company.job_detail_container_tag
        container_class = job.company.job_detail_container_class
        container_id = job.company.job_detail_container_id

        if container_id and container_class:
            soup = page_soup.find(container_tag, container_class, id=container_id)
        elif container_class:
            soup = page_soup.find(container_tag, container_class)
        elif container_id:
            soup = page_soup.find(container_tag, id=container_id)
        else:
            soup = page_soup.find(container_tag)

        if soup is None:
            log += f"No bs4 object found for job {job.pk}: {job.source_url}"
            continue

        job.body = markdownify.markdownify(soup.decode())
        job.save()

    if log:
        Bot.to_admin("Updating job attrs\n" + log)
