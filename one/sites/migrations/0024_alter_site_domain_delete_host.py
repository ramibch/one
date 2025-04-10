# Generated by Django 5.1.4 on 2025-01-18 11:06

from django.db import migrations, models

import one.sites.models


class Migration(migrations.Migration):

    dependencies = [
        ("sites", "0023_rename_name_site_domain"),
    ]

    operations = [
        migrations.AlterField(
            model_name="site",
            name="domain",
            field=models.CharField(
                db_index=True,
                max_length=32,
                unique=True,
                validators=[one.sites.models._simple_domain_name_validator],
                verbose_name="Name",
            ),
        ),
        migrations.DeleteModel(
            name="Host",
        ),
    ]
