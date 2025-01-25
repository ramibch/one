from django.conf import settings
from django.core.files import File
from django.utils.text import slugify
from huey import crontab
from huey.contrib import djhuey as huey

from one.base.utils.md import check_md_file_conventions

from ..base.utils.telegram import Bot
from ..sites.models import Site
from .models import Book, Chapter, ChapterFile


@huey.db_periodic_task(crontab(hour="3", minute="10"))
def sync_books(sites=None):
    """
    Sync books from specified sites
    """

    Book.sync_folders()

    # Definitions and checks
    submodule = Book.submodule
    submodule_path = Book.submodule_path
    sites = sites or Site.production.all()

    to_admin = f"🔄 Syncing {submodule}\n\n"

    for site in sites:
        to_admin += f"- {site.domain}:\n"

        # Scanning
        for book in site.books.all():
            folder = submodule_path / book.name

            for subfolder in folder.iterdir():
                if not subfolder.is_dir():
                    continue

                to_admin += f"✍ {book}/{subfolder.name}\n"

                chapter = Chapter.objects.get_or_create(
                    parent_folder=book,
                    subfolder_name=subfolder.name,
                    folder_name=book.name,
                )[0]

                lang_count = 0

                # Markdown files (.md) need to be processed first
                md_paths = (p for p in subfolder.iterdir() if p.name.endswith(".md"))
                for md_path in md_paths:
                    if not check_md_file_conventions(md_path):
                        to_admin += f"⚠️ File '{md_path.name}' does not meet conventions"
                        continue

                    lang_code = md_path.name[:2]
                    title = md_path.read_text().split("\n")[0].replace("#", "").strip()
                    body_text = "\n".join(md_path.read_text().split("\n")[1:]).strip()
                    setattr(chapter, f"title_{lang_code}", title)
                    setattr(chapter, f"slug_{lang_code}", slugify(title))
                    setattr(chapter, f"body_{lang_code}", body_text)
                    lang_count += 1

                # Files
                body_replacements = {}
                for file_path in (
                    p for p in subfolder.iterdir() if not p.name.endswith(".md")
                ):
                    if file_path.is_dir():
                        continue

                    db_file = ChapterFile.objects.get_or_create(
                        article=chapter,
                        name=file_path.name,
                    )[0]
                    db_file.file = File(file_path.open(mode="rb"), name=file_path.name)
                    db_file.save()
                    body_replacements[f"]({db_file.name})"] = f"]({db_file.file.url})"

                # Adjust body if markdown file includes files
                for local, remote in body_replacements.items():
                    for lang_code in settings.LANGUAGE_CODES:
                        field = f"body_{lang_code}"
                        ok = (
                            hasattr(chapter, field)
                            and getattr(chapter, field) is not None
                        )
                        if ok:
                            value = getattr(chapter, field).replace(local, remote)
                            setattr(chapter, f"body_{lang_code}", value)

                # Save object attributes in the database
                if lang_count > 0:
                    chapter.save()

    Bot.to_admin(to_admin)
