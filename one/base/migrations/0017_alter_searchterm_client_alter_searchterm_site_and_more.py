# Generated by Django 5.2rc1 on 2025-03-26 21:25

import auto_prefetch
import django.db.models.deletion
from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0016_searchterm"),
        ("clients", "0027_alter_client_country"),
        ("sites", "0032_remove_site_description_el_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="searchterm",
            name="client",
            field=auto_prefetch.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="clients.client",
            ),
        ),
        migrations.AlterField(
            model_name="searchterm",
            name="site",
            field=auto_prefetch.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, to="sites.site"
            ),
        ),
        migrations.AlterField(
            model_name="searchterm",
            name="user",
            field=auto_prefetch.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
