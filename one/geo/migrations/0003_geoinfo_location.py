# Generated by Django 5.2 on 2025-05-04 18:47

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("geo", "0002_googlegeoinfo"),
    ]

    operations = [
        migrations.AddField(
            model_name="geoinfo",
            name="location",
            field=django.contrib.gis.db.models.fields.PointField(
                blank=True, null=True, srid=4326
            ),
        ),
    ]
