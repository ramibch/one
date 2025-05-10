from http import HTTPStatus
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
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
    for c in Company.objects.filter(jobs_page_url__isnull=False):
        r = requests.get(c.jobs_page_url, headers=headers)
        if r.status_code != HTTPStatus.OK:
            log += f"{r.status_code} {c.jobs_page_url}"
            continue

        if c.jobs_page_html == r.text:
            continue

        c.jobs_page_html = r.text
        c.save()

        soup = BeautifulSoup(r.content.decode("utf-8"), "html.parser")

        if c.job_link_class:
            elements = soup.find_all("a", c.job_link_class, href=True)
        else:
            elements = soup.find_all("a", href=True)

        for element in elements:
            href = element.get("href")
            if not href:
                continue
            try:
                validate_url(href)
                url = href
            except ValidationError:
                purl = urlparse(r.url)
                url = f"{purl.scheme}//{purl.netloc}{href}"

            jobs.append(
                Job(
                    title=element.text[:64],
                    source_url=url,
                )
            )

    Job.objects.bulk_create(jobs, ignore_conflicts=True)

    if log:
        Bot.to_admin(log)
