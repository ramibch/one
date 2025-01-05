from factory import Faker
from factory.django import DjangoModelFactory

from .models import User


class UserFactory(DjangoModelFactory):
    username = Faker("word")
    email = Faker("email")
    is_active = Faker("boolean")
    password = Faker("password")
    is_superuser = False
    is_staff = False

    class Meta:
        model = User


class SuperuserFactory(UserFactory):
    is_superuser = True
    is_staff = True
