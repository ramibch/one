# Generated by Django 5.1.4 on 2024-12-29 02:48

import auto_prefetch
import django.db.models.deletion
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0016_rename_path_obj_request_path"),
        ("geo", "__first__"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="geoinfo",
            field=auto_prefetch.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="geo.geoinfo",
            ),
        ),
        migrations.DeleteModel(
            name="GeoInfo",
        ),
    ]