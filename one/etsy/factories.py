import factory
from django.contrib.auth import get_user_model
from django.utils.timezone import get_current_timezone
from factory.django import DjangoModelFactory

from .models import App, Shop, UserListing, UserShop, UserShopAuth

User = get_user_model()


class AppFactory(DjangoModelFactory):
    class Meta:
        model = App

    name = factory.Faker("company")
    keystring = factory.Faker("uuid4")
    redirect_uri = "https://ramib.ch/etsy/callback"
    scopes = factory.LazyFunction(lambda: ["listings_d", "listings_r", "listings_w"])


class UserShopAuthFactory(DjangoModelFactory):
    class Meta:
        model = UserShopAuth

    app = factory.SubFactory(AppFactory)
    user = factory.SubFactory("one.users.factories.UserFactory")
    etsy_user_id = factory.Faker("random_int", min=1000, max=9999)
    shop_id = factory.Faker("random_int", min=1000, max=9999)
    state = factory.Faker("uuid4")
    code_verifier = factory.Faker("uuid4")
    code = factory.Faker("uuid4")
    scopes = factory.LazyFunction(lambda: ["listings_d", "listings_r", "listings_w"])
    access_token = factory.Faker("uuid4")
    refresh_token = factory.Faker("uuid4")
    expires_at = factory.Faker("date_time", tzinfo=get_current_timezone())


class ShopFactory(DjangoModelFactory):
    class Meta:
        model = Shop

    user_shop_auth = factory.SubFactory(UserShopAuthFactory)
    name = factory.Faker("company")
    generic_listing_description = factory.Faker("text")
    price_percentage = 150


class UserShopFactory(DjangoModelFactory):
    class Meta:
        model = UserShop


class UserListingFactory(DjangoModelFactory):
    class Meta:
        model = UserListing

    user_shop = factory.SubFactory(UserShopFactory)
    user_shop_auth = factory.SubFactory(UserShopAuthFactory)
    quantity = 999
    title = factory.Faker("sentence")
    description = factory.Faker("paragraph")
    price = factory.Faker("pyfloat", left_digits=2, right_digits=2, positive=True)
    who_made = "i_did"
    when_made = "2020_2025"
    taxonomy_id = 12345
    listing_type = "download"
    tags = factory.LazyFunction(lambda: ["art", "digital", "print"])
