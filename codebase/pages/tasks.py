from pathlib import Path

from django.conf import settings
from django.db.models import Q
from django.utils.text import slugify
from huey import crontab
from huey.contrib import djhuey as huey

from ..base.telegram import Bot
from .models import Page


@huey.db_periodic_task(crontab(hour="2", minute="10"))
def sync_pages_dairly():
    """
    Read the contents of the 'pages' submodule and save them in the database.
    To know which contents to sync, check out the setting SYNC_PAGE_FOLDERS.
    """

    # definitions and checks
    to_admin = "🔄 Syncing pages\n\n"

    folders = getattr(settings, "SYNC_PAGE_FOLDERS", ())

    if len(folders) == 0:
        Bot.to_admin(to_admin + "No folders found while syncing pages. Check SYNC_PAGE_FOLDERS")
        return

    try:
        iter(folders)
    except TypeError:
        Bot.to_admin(to_admin + "The variable for folders is not iterable. Check SYNC_PAGE_FOLDERS")
        return

    pages_path = getattr(settings, "PAGES_MARKDOWN_PATH", None)

    if not isinstance(pages_path, Path):
        Bot.to_admin(to_admin + "No path for pages found. Check PAGES_MARKDOWN_PATH")
        return

    if not pages_path.is_dir():
        Bot.to_admin(to_admin + "The 'pages' path is not a directory. Check PAGES_MARKDOWN_PATH")
        return

    # Scanning
    for folder in folders:
        folder_path = pages_path / folder

        if not folder_path.is_dir():
            to_admin += f"🔴 {folder} is not listed\n\n"
            continue

        for subfolder_path in folder_path.iterdir():
            if not subfolder_path.is_dir():
                continue

            to_admin += f"✍ {folder}/{subfolder_path.name}\n"
            db_page = Page.objects.get_or_create(folder=folder, subfolder=subfolder_path.name)[0]

            # Markdown files (.md) need to be proccessed first
            for md_file_path in (p for p in subfolder_path.iterdir() if p.name.endswith(".md")):
                md_file_conventions_ok = all(
                    (
                        md_file_path.name[:2] in settings.LANGUAGE_CODES,
                        len(md_file_path.read_text().split("\n")) > 2,
                        md_file_path.read_text().strip().startswith("#"),
                    )
                )
                if not md_file_conventions_ok:
                    to_admin += f"⚠️ File '{md_file_path.name}' does not meet conventions"
                    continue

                lang_code = md_file_path.name[:2]
                title = md_file_path.read_text().split("\n")[0].replace("#", "").strip()
                body_text = "\n".join(md_file_path.read_text().split("\n")[1:]).strip()
                setattr(db_page, f"title_{lang_code}", title)
                setattr(db_page, f"slug_{lang_code}", slugify(title))
                setattr(db_page, f"body_{lang_code}", body_text)

            # Save all object attributes in the database
            db_page.save()

    # Delete articles that could not be processed
    qs = Page.objects.filter(Q(title__in=[None, ""]) | Q(body__in=[None, ""]))
    if qs.count() > 0:
        to_admin += "\nPages not possible to create:\n"
    for obj in qs:
        to_admin += f"{obj.folder}/{obj.subfolder}\n"
    qs.delete()

    Bot.to_admin(to_admin)
