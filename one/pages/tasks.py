from django.utils.text import slugify
from huey import crontab
from huey.contrib import djhuey as huey

from one.base.utils.md import check_md_file_conventions

from ..base.utils.telegram import Bot
from ..sites.models import Site
from .models import Page, PageParentFolder


@huey.db_periodic_task(crontab(hour="2", minute="10"))
def sync_pages(sites=None):
    """
    Sync of pages from specified sites
    """

    PageParentFolder.sync_folders()

    # Definitions and checks
    submodule = PageParentFolder.submodule
    submodule_path = PageParentFolder.submodule_path
    sites = sites or Site.production.all()
    to_admin = f"🔄 Syncing {submodule}\n\n"

    for site in sites:
        to_admin += f"- {site.name}:\n"

        # Scanning
        for db_folder in site.page_folders.all():
            folder = submodule_path / db_folder.name

            for subfolder in folder.iterdir():
                if not subfolder.is_dir():
                    continue

                to_admin += f"✍ {db_folder}/{subfolder.name}\n"

                page = Page.objects.get_or_create(
                    parent_folder=db_folder,
                    folder_name=db_folder.name,
                    subfolder_name=subfolder.name,
                )[0]

                # Markdown files (.md) need to be processed first
                md_paths = (p for p in subfolder.iterdir() if p.name.endswith(".md"))
                for md_path in md_paths:
                    if not check_md_file_conventions(md_path):
                        to_admin += f"⚠️ File '{md_path.name}' does not meet conventions"
                        continue

                    lang_code = md_path.name[:2]
                    title = md_path.read_text().split("\n")[0].replace("#", "").strip()
                    body_text = "\n".join(md_path.read_text().split("\n")[1:]).strip()
                    setattr(page, f"title_{lang_code}", title)
                    setattr(page, f"slug_{lang_code}", slugify(title))
                    setattr(page, f"body_{lang_code}", body_text)

                # Save all object attributes in the database
                page.save()

    Bot.to_admin(to_admin)
