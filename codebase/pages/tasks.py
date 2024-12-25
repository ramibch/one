from pathlib import Path

from django.conf import settings
from django.utils.text import slugify
from huey import crontab
from huey.contrib import djhuey as huey

from ..base.utils.telegram import Bot
from ..sites.models import Site
from .models import Page


@huey.task()
def trigger_sync_pages_task(sites):
    sync_pages_daily(sites=sites)


@huey.db_periodic_task(crontab(hour="2", minute="10"))
def sync_pages_daily(sites=None):
    """Sync of pages in the db."""
    # Definitions and checks
    submodule = "pages"
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
        for parent_folder_db_obj in site.page_folders.all():
            folder_path = submodule_path / parent_folder_db_obj.name

            if not folder_path.is_dir():
                to_admin += f"🔴 {parent_folder_db_obj} is not listed\n\n"
                continue

            for subfolder_path in folder_path.iterdir():
                if not subfolder_path.is_dir():
                    continue

                to_admin += f"✍ {parent_folder_db_obj}/{subfolder_path.name}\n"

                db_object = Page.objects.get_or_create(
                    parent_folder=parent_folder_db_obj,
                    subfolder_name=subfolder_path.name,
                    folder_name=parent_folder_db_obj.name,
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

                # Save all object attributes in the database
                db_object.save()

        Bot.to_admin(to_admin)
