from django.apps import apps as global_apps


def create_necessary_links(app_config, apps=global_apps, **kwargs):
    from ..models import Link

    Link.objects.sync_django_paths()
