from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from content.models import Article, ArticleFile, Topic

HOME_LISTING_TOPICS = [
    "django",
    "excel",
    "matlab",
    "htmx",
    "siemens",
    "git",
    "javascript",
    "devops",
    "linux",
    "mechanics",
    "physics",
]


class Command(BaseCommand):
    help = "Save in db articles written in Markdown."

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Processing...")

        root_path = settings.BASE_DIR / "material" / "articles"

        # Language
        for lang_path in root_path.iterdir():
            if lang_path.name not in settings.LANGUAGE_CODES:
                raise CommandError(f"Unknown language: {lang_path.name}")
            lang = lang_path.name

            # Topic (main topic)
            for topic_path in lang_path.iterdir():
                try:
                    topic = Topic.objects.get(slug=topic_path.name)
                except Topic.DoesNotExist:
                    raise CommandError(f"Topic does not exist: {topic_path.name}")

                home_listing = topic_path.name in HOME_LISTING_TOPICS

                # Object (data related to the model object)
                for obj_path in topic_path.iterdir():
                    self.stdout.write(f'Processing "{obj_path.name}"...')
                    create_or_update_article(lang, topic, obj_path, home_listing)

        self.stdout.write("Done.")


def create_or_update_article(lang, topic, article_path, home_listing):
    file_paths = [x for x in article_path.iterdir() if x.is_file()]
    if not (article_path / "body.md").is_file():
        return

    with open(article_path / "body.md", "r", encoding="utf-8") as f:
        body = f.read()

    try:
        a = Article.objects.get(title=article_path.name)
        if a.body == body:
            return
        a.body = body
        a.topic = topic
        a.language = lang
        a.home_listing = home_listing
        a.save()
    except Article.DoesNotExist:
        a = Article.objects.create(
            title=article_path.name,
            description=article_path.name,
            body=body,
            language=lang,
            topic=topic,
            home_listing=home_listing,
        )

    articlefile_paths = [x for x in file_paths if not x.name.endswith(".md")]
    body_replacements = {}
    for fpath in articlefile_paths:
        try:
            af = ArticleFile.objects.get(article=a, name=fpath.name)
            af.file.seek(0)
            if af.file.read() != fpath.read_bytes():
                af.file = File(fpath.open(mode="rb"), name=fpath.name)
                af.save()
        except ArticleFile.DoesNotExist:
            af = ArticleFile.objects.create(
                article=a,
                name=fpath.name,
                file=File(fpath.open(mode="rb"), name=fpath.name),
            )
        except ArticleFile.MultipleObjectsReturned:
            ArticleFile.objects.filter(article=a, name=fpath.name).delete()
            af = ArticleFile.objects.create(
                article=a,
                name=fpath.name,
                file=File(fpath.open(mode="rb"), name=fpath.name),
            )

        body_replacements[f"]({fpath.name})"] = f"]({af.file.url})"

    if body_replacements != {}:
        for local, remote in body_replacements.items():
            a.body = a.body.replace(local, remote)
        a.save()
