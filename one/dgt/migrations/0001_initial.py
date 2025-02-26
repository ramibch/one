# Generated by Django 5.1.4 on 2025-01-11 22:12

import auto_prefetch
import django.db.models.deletion
import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("sessions", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Question",
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
                ("title", models.TextField(max_length=256)),
                ("option_a", models.CharField(max_length=128)),
                ("option_b", models.CharField(max_length=128)),
                ("option_c", models.CharField(max_length=128)),
                ("correct_option", models.CharField(max_length=1)),
                ("explanation", models.TextField(max_length=512, null=True)),
                ("img_alt", models.CharField(max_length=128, null=True)),
                ("img_url", models.URLField(max_length=128)),
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
            name="Test",
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
                ("source_url", models.URLField(max_length=128)),
                ("title", models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name="SessionTest",
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
                    "session",
                    auto_prefetch.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sessions.session",
                    ),
                ),
                (
                    "test",
                    auto_prefetch.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dgt.test",
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
            name="SessionQuestion",
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
                ("selected_option", models.CharField(max_length=1)),
                ("is_correct", models.BooleanField(default=False)),
                (
                    "question",
                    auto_prefetch.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="dgt.question"
                    ),
                ),
                (
                    "session",
                    auto_prefetch.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sessions.session",
                    ),
                ),
                (
                    "session_test",
                    auto_prefetch.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dgt.sessiontest",
                    ),
                ),
                (
                    "test",
                    auto_prefetch.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="dgt.test"
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
        migrations.AddField(
            model_name="question",
            name="test",
            field=auto_prefetch.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="dgt.test"
            ),
        ),
    ]
