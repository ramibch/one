# Generated by Django 5.1.4 on 2025-03-10 21:23

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0014_etsyshop_created_on_etsyshop_updated_on"),
    ]

    operations = [
        migrations.AddField(
            model_name="etsylisting",
            name="created_on",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="etsylisting",
            name="updated_on",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
