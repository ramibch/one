import requests
from django.conf import settings
from django.core.files import File
from django.core.management import call_command
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from huey import crontab
from huey.contrib import djhuey as huey

from utils.telegram import report_to_admin

from .listings import LISTINGS_PATH, Listing
from .models import Article, ListingProduct, ListingTag

medium_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Host": "api.medium.com",
    "Authorization": f"Bearer {settings.MEDIUM_TOKEN}",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
}


@huey.db_periodic_task(crontab(hour="0", minute="30"))
def django_commands():
    call_command("compilemessages", ignore=["venv", "material"], locale=["de", "es"])


@huey.db_periodic_task(crontab(day_of_week="2", hour="12", minute="7"))
def publish_article_on_medium():
    articles = Article.objects.filter(published_in_medium=False, public=True)
    if articles.count() < 1:
        report_to_admin("⚠ No more articles to publish in Medium.")
        return

    a = articles[0]

    content = a.body + "\n\n"
    content += "Rami Boutassghount \n\n"
    content += f"[{settings.WEBSITE_LABEL}]({settings.WEBSITE_URL}) \n\n"
    content += f"[{settings.LINKEDIN_LABEL}]({settings.LINKEDIN_URL}) \n\n"
    content += f"[{settings.TWITTER_LABEL}]({settings.TWITTER_URL}) \n\n"
    content += f"[{settings.GITHUB_LABEL}]({settings.GITHUB_URL}) \n\n"

    data = {
        "title": a.title,
        "content": content,
        "contentFormat": "markdown",
        "publishStatus": "public",
    }

    url = f"https://api.medium.com/v1/users/{settings.MEDIUM_AUTHOR_ID}/posts"
    response = requests.post(url, headers=medium_headers, data=data)
    if response.status_code in [200, 201]:
        a.published_in_medium = True
        a.save()
        report_to_admin(f"Published article in Medium: {a.title}")

    if response.status_code == 429:
        # In [4]: r.text
        # Out[4]: '{"errors":[{"message":"User has reached the rate limit for publishing today.","code":1007}]}'
        report_to_admin(f"Medium Error 429 (reached the rate limit): {a.title}")

    if response.status_code == 403:
        report_to_admin(f"Medium Error 403 (Blocked): {a.title}")
    report_to_admin(response.text)


def get_medium_author_id():
    """uses the /me medium api to get the user's author id"""
    response = requests.get(
        "https://api.medium.com/v1/me",
        headers=medium_headers,
        params={"Authorization": f"Bearer {settings.MEDIUM_TOKEN}"},
    )
    if response.status_code == 200:
        return response.json()["data"]["id"]


def get_listings():
    dirnames = (p.name for p in LISTINGS_PATH.iterdir())
    for dirname in dirnames:
        try:
            yield Listing.objects.get(dirname=dirname)
        except Exception as e:
            report_to_admin(f"❌ Error getting the listing {dirname}: {e}")


@huey.db_periodic_task(crontab(hour="5", minute="30"))
def upload_listings_to_etsy():
    reporting = "Uploading and creating products from listings:" + "\n\n"
    for listing in get_listings():
        if listing.etsy_id != 0:
            continue
        try:
            listing.upload_to_etsy()
        except Exception as e:
            reporting += f"❌ Etsy upload error with {listing.dirname}: {e}\n"
    report_to_admin(reporting)


@huey.db_periodic_task(crontab(hour="9", minute="30"))
def sync_listingtags():
    reporting = "Sync main listing tags\n\n"
    tag_number = 3  # number of tags

    for listing in get_listings():
        if listing.lang != "en" or len(listing.tags) < tag_number:
            continue
        for tag in listing.tags[:tag_number]:
            with translation.override("de"):
                tag_de = str(_(tag))
            with translation.override("es"):
                tag_es = str(_(tag))
            kwargs = {"name_en": tag, "name_es": tag_es, "name_de": tag_de}
            try:
                ListingTag.objects.get(**kwargs)
            except ListingTag.DoesNotExist:
                ListingTag.objects.create(**kwargs)
            except Exception as e:
                reporting += f"⚠️ Error with {tag}: {e}\n"
            del kwargs
    reporting += "✅ Done"
    report_to_admin(reporting)


@huey.db_periodic_task(crontab(hour="10", minute="30"))
def sync_listings():
    reporting = "Sync listings between db and file system:" + "\n\n"
    for listing in get_listings():
        with translation.override(listing.lang):
            product = ListingProduct.objects.get_or_create(dirname=listing.dirname)[0]
            product.language = listing.lang
            try:
                image_path = list(listing.images_path.iterdir())[0]
            except IndexError:
                reporting += f"Image not found in {listing.dirname}\n"
                product.delete()
                continue

            if not image_path.is_file():
                reporting += f"Path doesn't correspond to a file: {listing.dirname}\n"
                product.delete()
                continue

            with open(image_path, "rb") as f:
                product.image.save(f"{listing.dirname}.png", File(f))

            tags = ListingTag.objects.filter(name__in=listing.tags)
            product.tags.add(*tags)
            product.save()
    reporting += "✅ Done"
    report_to_admin(reporting)


@huey.db_periodic_task(crontab(day_of_week="1", hour="10", minute="36"))
def check_gumroad_links():
    reporting = "Checking Gumroad links and listings:" + "\n\n"
    for listing in get_listings():
        if listing.gumroad_url == "":
            reporting += f"🔗 {listing.dirname} has no link\n"
            continue
        response = requests.get(listing.gumroad_url)
        if response.status_code == 404:
            reporting += f"❓ {listing.gumroad_url} not found\n"
            listing.gumroad_url = ""
        elif response.status_code == 200:
            pass
        else:
            reporting += f"⚠️ {listing.gumroad_url}, status: {response.status_code}\n"
            listing.gumroad_url = ""

    reporting += "✅ Done"
    report_to_admin(reporting)


@huey.db_periodic_task(crontab(minute="45"))
def promote_external_product():
    listing = ListingProduct.objects.filter(public=True, promoted=False).first()
    if listing is not None:
        listing.promote()
