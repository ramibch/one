import factory


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker("username")
    email = factory.Faker("email")
    password = "pass123"

    class Meta:
        model = "accounts.User"
        django_get_or_create = ("username",)
