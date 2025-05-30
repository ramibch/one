# Generated by Django 5.2 on 2025-05-04 18:53

import auto_prefetch
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0002_initial"),
        ("geo", "0003_geoinfo_location"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="geoinfo",
            field=auto_prefetch.ForeignKey(
                db_index=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="geo.geoinfo",
            ),
        ),
        migrations.AddIndex(
            model_name="client",
            index=models.Index(
                condition=models.Q(("geoinfo__isnull", False)),
                fields=["geoinfo"],
                name="client_geoinfo_fkey",
            ),
        ),
    ]
