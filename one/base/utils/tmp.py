from pathlib import Path

from django.conf import settings
from django.utils.functional import cached_property

from .telegram import Bot


class TmpFile:
    """
    Write from db file/image field in tmp folder file to be used by the file system.
    """

    TMP_DIR = settings.TMP_DIR

    def __init__(self, field):
        self.field = field
        self._path: Path = self.TMP_DIR / self.field.name

    def write_content_in_path(self) -> None:
        Path(self._path).parent.mkdir(exist_ok=True, parents=True)
        content = self.file_bytes
        with open(self._path, "wb") as f:
            f.write(content)

    @cached_property
    def file_bytes(self):
        try:
            self.field.storage.open(self.field.name, "rb").read()
        except FileNotFoundError:
            model_obj = self.field.instance
            Bot.to_admin(f"File not found for: PK={model_obj.pk} {type(model_obj)}")
            raise

    def path_exists(self):
        return self._path.is_file()

    @cached_property
    def path(self):
        if not self.path_exists():
            self.write_content_in_path()
        return self._path
