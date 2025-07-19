from pathlib import Path

from one.bot import Bot


class TmpFile:
    """
    Write from db file/image field in tmp folder file to be used by the file system.
    """

    TMP_DIR = Path("/tmp/django-one")
    PURGE_DAYS = 30

    def __init__(self, field):
        self.field = field
        self._path: Path = self.TMP_DIR / self.field.name

    def write_content_in_path(self) -> None:
        Path(self._path).parent.mkdir(exist_ok=True, parents=True)
        content = self.file_bytes
        with open(self._path, "wb") as f:
            f.write(content)

    @property
    def file_bytes(self):
        try:
            return self.field.storage.open(self.field.name, "rb").read()
        except FileNotFoundError as e:
            obj = self.field.instance
            Bot.to_admin(f"File not found for: pk={obj.pk} {type(obj)}: {e}")
            raise e

    def path_exists(self):
        return self._path.is_file()

    @property
    def path(self):
        if not self.path_exists():
            self.write_content_in_path()
        return self._path
