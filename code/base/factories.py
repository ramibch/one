import factory


class NavbarItemFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("lorem")

    class Meta:
        model = "base.NavbarItem"
