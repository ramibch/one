# Generated by Django 5.1.4 on 2024-12-21 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0003_initial"),
        ("sites", "0007_alter_site_default_language_and_more"),
        ("users", "0002_alter_user_language"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Language",
        ),
    ]
