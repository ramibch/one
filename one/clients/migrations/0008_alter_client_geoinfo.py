# Generated by Django 5.1.4 on 2024-12-25 07:05

import auto_prefetch
import django.db.models.deletion
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0007_alter_geoinfo_city_alter_geoinfo_continent_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="geoinfo",
            field=auto_prefetch.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="clients.geoinfo",
            ),
        ),
    ]
