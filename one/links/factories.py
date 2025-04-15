from django.conf import settings
from factory import Iterator, LazyAttribute
from factory.django import DjangoModelFactory
from faker import Faker

from .models import PATH_NAMES, Link

faker = Faker()


class LinkFactory(DjangoModelFactory):
    class Meta:
        model = Link

    language = Iterator(settings.LANGUAGE_CODES)
    languages = ["en", "de", "es"]
    custom_title = LazyAttribute(lambda _: faker.sentence())
    external_url = LazyAttribute(lambda _: faker.url())
    url_path = Iterator([p[0] for p in PATH_NAMES])
    topic = Iterator([t[0] for t in settings.TOPICS])
