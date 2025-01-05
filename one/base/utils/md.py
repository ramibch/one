from django.conf import settings


def check_md_file_conventions(md_path):
    return all(
        (
            md_path.name[:2] in settings.LANGUAGE_CODES,
            len(md_path.read_text().split("\n")) > 2,
            md_path.read_text().strip().startswith("#"),
        )
    )
