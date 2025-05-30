# Generated by Django 5.2 on 2025-04-26 09:29

import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Animation",
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
                (
                    "animation_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("vanilla", "Vanilla"),
                            ("onmouseover", "On event: onmouseover"),
                        ],
                        default="vanilla",
                        max_length=16,
                        null=True,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("bounce", "Bounce"),
                            ("flash", "Flash"),
                            ("pulse", "Pulse"),
                            ("rubberBand", "Rubber Band"),
                            ("shakeX", "Shake X"),
                            ("shakeY", "Shake Y"),
                            ("headShake", "Head Shake"),
                            ("swing", "Swing"),
                            ("tada", "Tada"),
                            ("wobble", "Wobble"),
                            ("jello", "Jello"),
                            ("heartBeat", "Heart Beat"),
                        ],
                        default="flash",
                        max_length=16,
                        null=True,
                    ),
                ),
                (
                    "repeat",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("repeat-1", "1 Time"),
                            ("repeat-2", "2 Times"),
                            ("repeat-3", "3 Times"),
                            ("infinite", "Infinite times"),
                        ],
                        default="repeat-1",
                        max_length=16,
                        null=True,
                    ),
                ),
                (
                    "speed",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("slow", "Slow 2s"),
                            ("slower", "Slow 3s"),
                            ("fast", "Fast 800ms"),
                            ("faster", "Faster 500ms"),
                        ],
                        max_length=16,
                        null=True,
                    ),
                ),
                (
                    "delay",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("2s", "2 Seconds"),
                            ("3s", "3 Seconds"),
                            ("4s", "4 Seconds"),
                            ("5s", "5 Seconds"),
                        ],
                        max_length=16,
                        null=True,
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
            name="ContactMessage",
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
                ("name", models.CharField(max_length=128, verbose_name="Your name")),
                (
                    "email",
                    models.EmailField(max_length=128, verbose_name="Email address"),
                ),
                ("message", models.TextField(max_length=1000, verbose_name="Message")),
                ("created_on", models.DateTimeField(auto_now_add=True)),
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
            name="SearchTerm",
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
                ("query", models.TextField()),
                ("created_on", models.DateTimeField(auto_now_add=True)),
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
