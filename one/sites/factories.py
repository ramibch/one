import factory
from django.conf import settings
from factory.django import DjangoModelFactory
from faker import Faker

from .models import PicoCssColor, Site

faker = Faker()


class SiteFactory(DjangoModelFactory):
    class Meta:
        model = Site

    language = factory.Iterator(settings.LANGUAGE_CODES)
    languages = ["en", "es", "de"]  # TODO: improve
    domain = factory.LazyAttribute(lambda _: faker.domain_name())
    remarks = factory.LazyAttribute(lambda _: faker.sentence())
    brand_name = factory.LazyAttribute(lambda _: faker.company())
    emoji = factory.Iterator(["✅", "🌐", "🚀", "🎁", "🦊"])
    emoji_in_brand = factory.LazyAttribute(lambda _: faker.boolean())
    picocss_color = factory.Iterator(PicoCssColor.values)
    footer_links_separator = factory.Iterator(["|", "-"])
    change_theme_light_in_footer = factory.LazyAttribute(lambda _: faker.boolean())
    change_theme_light_in_navbar = factory.LazyAttribute(lambda _: faker.boolean())
    change_language_in_navbar = factory.LazyAttribute(lambda _: faker.boolean())
    change_language_in_footer = factory.LazyAttribute(lambda _: faker.boolean())

    spam_requests_duration = factory.LazyAttribute(lambda _: faker.time_delta())
    requests_duration = factory.LazyAttribute(lambda _: faker.time_delta())

    # TODO:
    # article_folders = ManyToManyField("articles.ArticleParentFolder", blank=True)
    # page_folders = ManyToManyField("pages.PageParentFolder", blank=True)
    # books = ManyToManyField("books.Book", blank=True)

    title = factory.LazyAttribute(lambda _: faker.sentence())
    description = factory.LazyAttribute(lambda _: faker.text())
    keywords = factory.LazyAttribute(lambda _: faker.sentence())
