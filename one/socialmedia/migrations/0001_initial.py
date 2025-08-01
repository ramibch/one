# Generated by Django 5.2.4 on 2025-07-28 20:33

import auto_prefetch
import django.db.models.deletion
import django.db.models.manager
import one.db
import secrets
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LinkedinAuth",
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
                ("state", models.CharField(default=secrets.token_hex, max_length=128)),
                ("code", models.TextField(blank=True, null=True)),
                (
                    "access_token",
                    models.TextField(blank=True, editable=False, null=True),
                ),
                ("expires_at", models.DateTimeField(blank=True, null=True)),
                (
                    "refresh_token",
                    models.TextField(blank=True, editable=False, null=True),
                ),
                (
                    "refresh_token_expires_at",
                    models.DateTimeField(blank=True, null=True),
                ),
                ("scope", models.TextField(blank=True, null=True)),
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
        migrations.CreateModel(
            name="MastodonChannel",
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
                ("name", models.CharField(max_length=64)),
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
                    "language",
                    models.CharField(
                        choices=[
                            ("en", "English"),
                            ("de", "German"),
                            ("es", "Spanish"),
                            ("fr", "French"),
                            ("it", "Italian"),
                            ("nl", "Dutch"),
                            ("pt", "Portuguese"),
                        ],
                        default="en",
                        max_length=4,
                    ),
                ),
                ("access_token", models.CharField(max_length=256)),
                ("api_base_url", models.URLField(max_length=256)),
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
        migrations.CreateModel(
            name="SocialMediaPost",
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
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=256)),
                ("text", models.TextField()),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="socialmedia/"),
                ),
                (
                    "image_li_urn",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("scheduled_at", models.DateTimeField(blank=True, null=True)),
                ("sent_at", models.DateTimeField(blank=True, null=True)),
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
                    "status",
                    models.CharField(
                        choices=[
                            ("draft", "Draft"),
                            ("scheduled", "Scheduled"),
                            ("sent", "Sent"),
                            ("failed", "Failed"),
                        ],
                        default="draft",
                        max_length=16,
                    ),
                ),
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
        migrations.CreateModel(
            name="TwitterChannel",
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
                ("name", models.CharField(max_length=64)),
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
                    "language",
                    models.CharField(
                        choices=[
                            ("en", "English"),
                            ("de", "German"),
                            ("es", "Spanish"),
                            ("fr", "French"),
                            ("it", "Italian"),
                            ("nl", "Dutch"),
                            ("pt", "Portuguese"),
                        ],
                        default="en",
                        max_length=4,
                    ),
                ),
                ("bearer_token", models.CharField(max_length=256)),
                ("api_key", models.CharField(max_length=256)),
                ("api_key_secret", models.CharField(max_length=256)),
                ("access_token", models.CharField(max_length=256)),
                ("access_token_secret", models.CharField(max_length=256)),
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
        migrations.CreateModel(
            name="LinkedinChannel",
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
                ("name", models.CharField(max_length=64)),
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
                    "language",
                    models.CharField(
                        choices=[
                            ("en", "English"),
                            ("de", "German"),
                            ("es", "Spanish"),
                            ("fr", "French"),
                            ("it", "Italian"),
                            ("nl", "Dutch"),
                            ("pt", "Portuguese"),
                        ],
                        default="en",
                        max_length=4,
                    ),
                ),
                ("author_id", models.CharField(max_length=32)),
                (
                    "author_type",
                    models.CharField(
                        choices=[
                            ("person", "Person"),
                            ("organization", "Organization"),
                        ],
                        max_length=32,
                    ),
                ),
                (
                    "auth",
                    auto_prefetch.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="socialmedia.linkedinauth",
                    ),
                ),
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
        migrations.CreateModel(
            name="LinkedinGroupChannel",
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
                ("name", models.CharField(max_length=64)),
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
                    "language",
                    models.CharField(
                        choices=[
                            ("en", "English"),
                            ("de", "German"),
                            ("es", "Spanish"),
                            ("fr", "French"),
                            ("it", "Italian"),
                            ("nl", "Dutch"),
                            ("pt", "Portuguese"),
                        ],
                        default="en",
                        max_length=4,
                    ),
                ),
                ("group_id", models.CharField(max_length=64, unique=True)),
                ("is_private", models.BooleanField(default=True)),
                (
                    "channel",
                    auto_prefetch.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="socialmedia.linkedinchannel",
                    ),
                ),
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
