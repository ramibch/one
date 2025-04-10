# Generated by Django 5.1 on 2025-03-15 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0016_etsylisting_include_generic_description"),
    ]

    operations = [
        migrations.RenameField(
            model_name="etsyshop",
            old_name="default_language",
            new_name="language",
        ),
        migrations.RenameField(
            model_name="product",
            old_name="default_language",
            new_name="language",
        ),
        migrations.AddField(
            model_name="product",
            name="is_draft",
            field=models.BooleanField(default=True),
        ),
    ]
