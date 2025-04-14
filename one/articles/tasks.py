from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.utils.text import slugify
from huey import crontab
from huey.contrib import djhuey as huey

from one.base.utils.md import check_md_file_conventions

from ..base.utils.telegram import Bot
from ..sites.models import Site
from .models import Article, ArticleFile, MainTopic


@huey.db_periodic_task(crontab(hour="1", minute="10"))
def sync_articles(sites=None):
    """
    Sync articles from the submodules 'articles'
    """

    MainTopic.sync_folders()

    submodule = MainTopic.submodule
    submodule_path: Path = MainTopic.submodule_path
    sites = sites or Site.objects.all()

    to_admin = f"🔄 Syncing {submodule}\n\n"

    # Scanning
    for maintopic in MainTopic.objects.all():
        folder: Path = submodule_path / maintopic.name

        if not folder.is_dir():
            maintopic.present_in_filesystem = False
            maintopic.save()
            continue

        for subfolder in folder.iterdir():
            if not subfolder.is_dir():
                continue

            to_admin += f"✍ {maintopic}/{subfolder.name}\n"

            article = Article.objects.get_or_create(
                parent_folder=maintopic,
                subfolder_name=subfolder.name,
                folder_name=maintopic.name,
            )[0]
            lang_count = 0
            # Markdown files (.md) need to be processed first
            md_paths = (p for p in subfolder.iterdir() if p.name.endswith(".md"))
            for md_path in md_paths:
                if not check_md_file_conventions(md_path):
                    to_admin += f"⚠️ File '{md_path.name}' does not meet conventions\n"
                    continue

                lang_code = md_path.name[:2]
                title = md_path.read_text().split("\n")[0].replace("#", "").strip()
                body_text = "\n".join(md_path.read_text().split("\n")[1:]).strip()
                setattr(article, f"title_{lang_code}", title)
                setattr(article, f"slug_{lang_code}", slugify(title))
                setattr(article, f"body_{lang_code}", body_text)
                article.languages.append(lang_code)
                lang_count += 1

            # Files
            body_replacements = {}
            for file_path in (
                p for p in subfolder.iterdir() if not p.name.endswith(".md")
            ):
                if file_path.is_dir():
                    continue

                db_file = ArticleFile.objects.get_or_create(
                    article=article,
                    name=file_path.name,
                )[0]

                with file_path.open(mode="rb") as f:
                    db_file.file = File(f, name=file_path.name)
                    db_file.save()
                body_replacements[f"]({db_file.name})"] = f"]({db_file.file.url})"

            # Adjust body if markdown file includes files
            for local, remote in body_replacements.items():
                for lang_code in settings.LANGUAGE_CODES:
                    field = f"body_{lang_code}"
                    ok = hasattr(article, field) and getattr(article, field) is not None
                    if ok:
                        value = getattr(article, field).replace(local, remote)
                        setattr(article, f"body_{lang_code}", value)

            # Save object attributes in the database
            if lang_count > 0:
                article.save()

    Bot.to_admin(to_admin)
