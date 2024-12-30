from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.utils.text import slugify
from huey import crontab
from huey.contrib import djhuey as huey

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
    submodule = "books"
    submodule_path = settings.SUBMODULES_PATH / submodule

    if not isinstance(submodule_path, Path):
        Bot.to_admin(f"No path for {submodule} found. Check SUBMODULES_PATH")
        return

    if not submodule_path.is_dir():
        Bot.to_admin(f"The '{submodule}' path is not a directory.")
        return

    if sites is None:
        sites = Site.objects.filter()

    for site in sites:
        to_admin = f"🔄 Syncing {submodule} for {site.name}\n\n"

        # Scanning
        for book in site.books.all():
            folder_path = submodule_path / book.name

            if not folder_path.is_dir():
                to_admin += f"🔴 {book} is not listed\n\n"
                continue

            for subfolder_path in folder_path.iterdir():
                if not subfolder_path.is_dir():
                    continue

                to_admin += f"✍ {book}/{subfolder_path.name}\n"

                db_object = Chapter.objects.get_or_create(
                    parent_folder=book,
                    subfolder_name=subfolder_path.name,
                    folder_name=book.name,
                )[0]

                # Markdown files (.md) need to be processed first
                for md_file_path in (
                    p for p in subfolder_path.iterdir() if p.name.endswith(".md")
                ):
                    md_file_conventions_ok = all(
                        (
                            md_file_path.name[:2] in settings.LANGUAGE_CODES,
                            len(md_file_path.read_text().split("\n")) > 2,
                            md_file_path.read_text().strip().startswith("#"),
                        )
                    )
                    if not md_file_conventions_ok:
                        to_admin += (
                            f"⚠️ File '{md_file_path.name}' does not meet conventions"
                        )
                        continue

                    lang_code = md_file_path.name[:2]
                    title = (
                        md_file_path.read_text().split("\n")[0].replace("#", "").strip()
                    )
                    body_text = "\n".join(
                        md_file_path.read_text().split("\n")[1:]
                    ).strip()
                    setattr(db_object, f"title_{lang_code}", title)
                    setattr(db_object, f"slug_{lang_code}", slugify(title))
                    setattr(db_object, f"body_{lang_code}", body_text)

                # Files
                body_replacements = {}
                for file_path in (
                    p for p in subfolder_path.iterdir() if not p.name.endswith(".md")
                ):
                    db_file = ChapterFile.objects.get_or_create(
                        article=db_object,
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
                            hasattr(db_object, field)
                            and getattr(db_object, field) is not None
                        )
                        if ok:
                            new_value = getattr(db_object, field).replace(local, remote)
                            setattr(db_object, f"body_{lang_code}", new_value)

                # Save all object attributes in the database
                db_object.save()

        Bot.to_admin(to_admin)
