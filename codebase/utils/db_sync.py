from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.db.models import Q
from django.utils.text import slugify

from ..base.models import ExtendedSite
from .telegram import Bot


def sync_model_objects(folders_setting, model_class, file_class=None):
    """
    Read the contents of the specified submodule and save them in the database.
    :param folders_setting: str, setting name for folders to sync.
    :param model_class: Model class to save objects (Page or Article).
    :param file_class: Optional, file model class (ArticleFile for articles).
    """

    # Determine model type and paths based on the model class's meta attributes
    model_type = model_class._meta.model_name
    markdown_path = getattr(settings, "SUBMODULES_PATH", None) / f"{model_type}s"

    # Definitions and checks
    for extsite in ExtendedSite.objects.filter():
        to_admin = f"🔄 Syncing {model_type}s for {extsite.name}\n\n"

        folders = getattr(settings, folders_setting, ())  # TODO: this depends now on the Site instances.

        if not folders:
            Bot.to_admin(to_admin + f"No folders found while syncing {model_type}s. Check {folders_setting}")
            return

        try:
            iter(folders)
        except TypeError:
            Bot.to_admin(to_admin + f"The variable for folders is not iterable. Check {folders_setting}")
            return

        if not isinstance(markdown_path, Path):
            Bot.to_admin(to_admin + f"No path for {model_type}s found. Check SUBMODULES_PATH")
            return
        if not markdown_path.is_dir():
            Bot.to_admin(to_admin + f"The '{model_type}' path is not a directory. Check SUBMODULES_PATH")
            return

        # Scanning
        for folder in folders:
            folder_path = markdown_path / folder

            if not folder_path.is_dir():
                to_admin += f"🔴 {folder} is not listed\n\n"
                continue

            for subfolder_path in folder_path.iterdir():
                if not subfolder_path.is_dir():
                    continue

                body_replacements = {} if model_type == "article" else None
                to_admin += f"✍ {folder}/{subfolder_path.name}\n"
                db_object = model_class.objects.get_or_create(folder=folder, subfolder=subfolder_path.name)[0]

                # Markdown files (.md) need to be processed first
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
                    setattr(db_object, f"title_{lang_code}", title)
                    setattr(db_object, f"slug_{lang_code}", slugify(title))
                    setattr(db_object, f"body_{lang_code}", body_text)

                # Process additional files if model is 'article'
                if model_type == "article" and file_class:
                    for other_file_path in (p for p in subfolder_path.iterdir() if not p.name.endswith(".md")):
                        db_file = file_class.objects.get_or_create(article=db_object, name=other_file_path.name)[0]
                        db_file.file = File(other_file_path.open(mode="rb"), name=other_file_path.name)
                        db_file.save()
                        body_replacements[f"]({db_file.name})"] = f"]({db_file.file.url})"

                    # Adjust body if markdown file includes files
                    for local, remote in body_replacements.items():
                        for lang_code in settings.LANGUAGE_CODES:
                            new_value = getattr(db_object, f"body_{lang_code}").replace(local, remote)
                            setattr(db_object, f"body_{lang_code}", new_value)

                # Save all object attributes in the database
                db_object.save()

        # Delete objects that could not be processed
        qs = model_class.objects.filter(Q(title__in=[None, ""]) | Q(body__in=[None, ""]))
        if qs.exists():
            to_admin += f"\n{model_type.capitalize()}s not possible to create:\n"
        for obj in qs:
            to_admin += f"{obj.folder}/{obj.subfolder}\n"
        qs.delete()

        Bot.to_admin(to_admin)
