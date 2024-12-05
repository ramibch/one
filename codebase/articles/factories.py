import factory


class ArticlesFolderFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("word")

    class Meta:
        model = "articles.ArticlesFolder"
        django_get_or_create = ("name",)


class ArticleFactory(factory.django.DjangoModelFactory):
    submodule = factory.SubFactory(ArticlesFolderFactory)
    title = factory.Faker("sentence")
    slug = factory.Faker("slug")
    folder = factory.Faker("word")
    subfolder = factory.Faker("slug")
    body = factory.Faker("text")

    class Meta:
        model = "articles.Article"
        django_get_or_create = ("slug",)
