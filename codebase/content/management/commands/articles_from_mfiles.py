"""maybe create 'process_mfiles.py' > to generate articles + listing items"""

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from content.models import Topic

MATLAB_TOPIC = Topic.objects.get_or_create(name="Matlab")[0]


class Command(BaseCommand):
    help = "Convert .m files to body.md articles"

    @transaction.atomic
    def handle(self, *args, **options):
        # From: material/mfiles/<lang>/<mfile_path>
        # To: material/articles/<lang>/<topic>/<obj_related_folder>/

        self.stdout.write("Processing...")
        root_path = settings.BASE_DIR / "material" / "mfiles"

        # Language
        for lang_path in root_path.iterdir():
            if lang_path.name not in settings.LANGUAGE_CODES:
                raise CommandError(f"Unknown language: {lang_path.name}")
            lang = lang_path.name

            # Where the mfile is contained
            for m_dir in lang_path.iterdir():
                self.stdout.write(f'Processing "{m_dir.name}"...')
                process_mfile(lang, m_dir)

        self.stdout.write("Done.")


def process_mfile(lang, m_dir):
    file_paths = [x for x in m_dir.iterdir() if x.is_file()]
    try:
        m_file_path = [x for x in file_paths if x.name.endswith(".m")][0]
    except IndexError:
        return

    with open(m_file_path, "r", encoding="utf-8") as f:
        file_content = f.read()

    body = ""
    if lang == "es":
        body = f"Crea un archivo (_{m_file_path.name}_) en tu carpeta de trabajo de Matlab con el siguiente código:\n\n"
    elif lang == "de":
        body = f"Erstell eine Datei (_{m_file_path.name}_) in deinem Matlab-Arbeitsordner mit dem folgenden Code:\n\n"
    elif "en" in lang:
        body = f"Create a file (_{m_file_path.name}_) in your Matlab working folder with the following code:\n\n"

    body += "```matlab\n\n"
    body += file_content
    body += "\n\n```\n"

    # Create a folder
    article_dir = (
        settings.BASE_DIR / "material" / "articles" / lang / "matlab" / m_dir.name
    )
    try:
        article_dir.mkdir()
    except FileExistsError:
        pass

    with open(article_dir / "body.md", "w", encoding="utf-8") as f:
        f.write(body)
