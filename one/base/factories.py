import factory
from factory.django import DjangoModelFactory
from faker import Faker

from one.clients.factories import ClientFactory
from one.sites.factories import SiteFactory

from .animations import (
    AnimationDelay,
    AnimationRepeat,
    AnimationSpeed,
    AnimationType,
    AttentionSeekers,
)
from .models import Animation

faker = Faker()


class SearchTerm(DjangoModelFactory):
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
