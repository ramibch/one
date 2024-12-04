import factory


class ArticlesFolderFactory(factory.django.DjangoModelFactory):
    name = factory.faker("word")

    class Meta:
        model = "articles.ArticlesFolder"
        django_get_or_create = ("name",)


class ArticleFactory(factory.django.DjangoModelFactory):
    submodule = factory.SubFactory(ArticlesFolderFactory)
    title = factory.faker("sentence")
    slug = factory.faker("slug")
    folder = factory.faker("word")
    subfolder = factory.faker("slug")
    body = factory.faker("text")

    class Meta:
        model = "articles.Article"
        django_get_or_create = ("slug",)
