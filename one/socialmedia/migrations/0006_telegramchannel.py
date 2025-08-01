# Generated by Django 5.2.4 on 2025-07-30 05:00

import django.db.models.manager
import one.db
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("socialmedia", "0005_remove_linkedingroupchannel_language_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="TelegramChannel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=128)),
                ("post_jobs", models.BooleanField(default=False)),
                ("post_english", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "topics",
                    one.db.ChoiceArrayField(
                        base_field=models.CharField(
                            choices=[
                                ("django", "Django"),
                                ("htmx", "htmx"),
                                ("alpinejs", "AlpineJS"),
                                ("devops", "DevOps"),
                                ("python", "Python"),
                                ("linux", "Linux"),
                                ("latex", "LaTex"),
                                ("matlab", "Matlab"),
                                ("siemens", "Siemens"),
                                ("excel", "Excel"),
                                ("maths", "Maths"),
                                ("mechanics", "Mechanics"),
                                ("english", "English"),
                                ("electronics", "Electronics"),
                                ("calendar", "Calendars"),
                                ("one", "One project"),
                            ],
                            max_length=16,
                        ),
                        blank=True,
                        default=list,
                        size=None,
                    ),
                ),
                (
                    "languages",
                    one.db.ChoiceArrayField(
                        base_field=models.CharField(
                            choices=[
                                ("en", "English"),
                                ("de", "German"),
                                ("es", "Spanish"),
                                ("fr", "French"),
                                ("it", "Italian"),
                                ("nl", "Dutch"),
                                ("pt", "Portuguese"),
                            ],
                            max_length=8,
                        ),
                        blank=True,
                        default=list,
                        size=None,
                    ),
                ),
                ("group_id", models.CharField(max_length=64, unique=True)),
            ],
            options={
                "abstract": False,
                "base_manager_name": "prefetch_manager",
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
        ),
    ]
