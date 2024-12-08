from django.apps import apps as global_apps


def create_languages_in_db(app_config, apps=global_apps, **kwargs):
    from ..models import Language

    Language.objects.sync_languages()
