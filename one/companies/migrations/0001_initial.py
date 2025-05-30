# Generated by Django 5.2 on 2025-05-04 18:40

import auto_prefetch
import django.db.models.deletion
import django.db.models.manager
import one.db
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("geo", "0002_googlegeoinfo"),
    ]

    operations = [
        migrations.CreateModel(
            name="Company",
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
                ("name", models.CharField(max_length=128, unique=True)),
                ("website", models.URLField(max_length=128)),
                ("jobs_url", models.CharField(blank=True, max_length=128, null=True)),
                ("remarks", models.TextField(blank=True, null=True)),
                (
                    "application_methods",
                    one.db.ChoiceArrayField(
                        base_field=models.CharField(
                            choices=[
                                ("email", "Email"),
                                ("website", "Own website"),
                                ("external", "External service"),
                            ],
                            max_length=32,
                        ),
                        blank=True,
                        default=list,
                        size=None,
                    ),
                ),
            ],
            options={
                "verbose_name": "company",
                "verbose_name_plural": "companies",
                "abstract": False,
                "base_manager_name": "prefetch_manager",
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name="CompanyLocation",
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
                    "company",
                    auto_prefetch.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="companies.company",
                    ),
                ),
                (
                    "geo_info",
                    auto_prefetch.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="geo.googlegeoinfo",
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
