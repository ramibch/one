import shutil

from django.conf import settings


def copy_texmf():
    shutil.rmtree(settings.DESTINATION_TEXMF_DIR, ignore_errors=False)
    shutil.copytree(settings.ORIGIN_TEXMF_DIR, settings.DESTINATION_TEXMF_DIR, dirs_exist_ok=True)
    print("✅ texmf copied successfully")
