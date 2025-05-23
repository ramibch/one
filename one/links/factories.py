from random import randint, sample

import factory
from django.conf import settings
from factory.django import DjangoModelFactory
from faker import Faker

from one.choices import Topics

from .models import PATH_NAMES, Link

faker = Faker()
LANGS = settings.LANGUAGE_CODES


class LinkFactory(DjangoModelFactory):
    class Meta:
        model = Link

    language = factory.Iterator(settings.LANGUAGE_CODES)
    languages = factory.List(sample(LANGS, k=randint(0, len(LANGS))))
    custom_title = factory.LazyAttribute(lambda _: faker.sentence())
    external_url = factory.LazyAttribute(lambda _: faker.url())
    url_path = factory.Iterator([p[0] for p in PATH_NAMES])
    topic = factory.Iterator([Topics.values])
