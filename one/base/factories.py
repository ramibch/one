from random import randint, sample

import factory
from django.conf import settings
from factory.django import DjangoModelFactory
from faker import Faker

from one.choices import Topics
from one.clients.factories import ClientFactory
from one.sites.factories import SiteFactory

from .animations import (
    AnimationDelay,
    AnimationRepeat,
    AnimationSpeed,
    AnimationType,
    AttentionSeekers,
)
from .models import PATH_NAMES, Animation, Link

faker = Faker()
LANGS = settings.LANGUAGE_CODES


class SearchTermFactory(DjangoModelFactory):
    query = factory.LazyAttribute(lambda _: faker.sentence())
    client = factory.SubFactory(ClientFactory)
    site = factory.SubFactory(SiteFactory)


class AnimationFactory(DjangoModelFactory):
    class Meta:
        model = Animation

    animation_type = factory.Iterator(AnimationType.values)
    name = factory.Iterator(AttentionSeekers.values)
    repeat = factory.Iterator(AnimationRepeat.values)
    speed = factory.Iterator(AnimationSpeed.values)
    delay = factory.Iterator(AnimationDelay.values)


class LinkFactory(DjangoModelFactory):
    class Meta:
        model = Link

    language = factory.Iterator(settings.LANGUAGE_CODES)
    languages = factory.List(sample(LANGS, k=randint(0, len(LANGS))))
    custom_title = factory.LazyAttribute(lambda _: faker.sentence())
    external_url = factory.LazyAttribute(lambda _: faker.url())
    url_path = factory.Iterator([p[0] for p in PATH_NAMES])
    topic = factory.Iterator([Topics.values])
