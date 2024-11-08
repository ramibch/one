# Generated by Django 5.1.3 on 2024-11-08 07:34

import django.contrib.sites.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("sites", "0002_alter_domain_unique"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExtendedSite",
            fields=[
                (
                    "site_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="sites.site",
                    ),
                ),
                ("remarks", models.TextField(blank=True, null=True)),
                ("emoji", models.CharField(max_length=8, null=True)),
                ("default_page_title", models.CharField(max_length=64, null=True)),
                ("default_page_title_en", models.CharField(max_length=64, null=True)),
                ("default_page_title_de", models.CharField(max_length=64, null=True)),
                ("default_page_title_es", models.CharField(max_length=64, null=True)),
                (
                    "default_page_description",
                    models.TextField(max_length=256, null=True),
                ),
                (
                    "default_page_description_en",
                    models.TextField(max_length=256, null=True),
                ),
                (
                    "default_page_description_de",
                    models.TextField(max_length=256, null=True),
                ),
                (
                    "default_page_description_es",
                    models.TextField(max_length=256, null=True),
                ),
                ("default_page_keywords", models.TextField(max_length=128, null=True)),
                (
                    "default_page_keywords_en",
                    models.TextField(max_length=128, null=True),
                ),
                (
                    "default_page_keywords_de",
                    models.TextField(max_length=128, null=True),
                ),
                (
                    "default_page_keywords_es",
                    models.TextField(max_length=128, null=True),
                ),
                ("emoji_in_brand", models.BooleanField(default=True)),
                ("change_theme_light_in_footer", models.BooleanField(default=True)),
                ("change_theme_light_in_navbar", models.BooleanField(default=True)),
                ("change_language_in_navbar", models.BooleanField(default=True)),
                ("change_language_in_footer", models.BooleanField(default=True)),
                ("last_huey_flush", models.DateTimeField(null=True)),
            ],
            bases=("sites.site",),
            managers=[
                ("objects", django.contrib.sites.models.SiteManager()),
            ],
        ),
    ]