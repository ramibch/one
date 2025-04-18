import factory
from django.conf import settings
from factory.django import DjangoModelFactory
from faker import Faker

from one.sites.factories import SiteFactory
from one.users.factories import UserFactory

from .models import Client

faker = Faker()


class ClientFactory(DjangoModelFactory):
    class Meta:
        model = Client

    user = factory.SubFactory(UserFactory)
    country = factory.Iterator(settings.COUNTRY_CODES)
    site = factory.SubFactory(SiteFactory)
    ip_address = factory.LazyAttribute(
        lambda _: faker.ipv4() if faker.boolean() else faker.ipv6()
    )
    is_blocked = factory.LazyAttribute(
        lambda _: faker.boolean(chance_of_getting_true=5)
    )
    user_agent = factory.LazyAttribute(lambda _: faker.user_agent())

    @factory.post_generation
    def post(obj: Client, create, extracted, **kwargs):
        obj.update_geo_values()
