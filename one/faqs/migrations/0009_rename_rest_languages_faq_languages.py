# Generated by Django 5.1.4 on 2025-01-26 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("faqs", "0008_rename_languages_faq_rest_languages"),
    ]

    operations = [
        migrations.RenameField(
            model_name="faq",
            old_name="rest_languages",
            new_name="languages",
        ),
    ]
