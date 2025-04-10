# Generated by Django 5.2 on 2025-04-07 20:19

import auto_prefetch
import django.db.models.deletion
import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0034_remove_home_template_name_remove_home_view_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="benefitssection",
            name="emoji",
        ),
        migrations.AddField(
            model_name="benefitssection",
            name="title",
            field=models.CharField(default="", max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="benefitssection",
            name="title_de",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="benefitssection",
            name="title_en",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="benefitssection",
            name="title_es",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="benefitssection",
            name="title_fr",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="benefitssection",
            name="title_it",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="benefitssection",
            name="title_nl",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="benefitssection",
            name="title_pt",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="problemsection",
            name="description_de",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="problemsection",
            name="description_en",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="problemsection",
            name="description_es",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="problemsection",
            name="description_fr",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="problemsection",
            name="description_it",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="problemsection",
            name="description_nl",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="problemsection",
            name="description_pt",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="problemsection",
            name="title_de",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="problemsection",
            name="title_en",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="problemsection",
            name="title_es",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="problemsection",
            name="title_fr",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="problemsection",
            name="title_it",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="problemsection",
            name="title_nl",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="problemsection",
            name="title_pt",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="solutionsection",
            name="description_de",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="solutionsection",
            name="description_en",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="solutionsection",
            name="description_es",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="solutionsection",
            name="description_fr",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="solutionsection",
            name="description_it",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="solutionsection",
            name="description_nl",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="solutionsection",
            name="description_pt",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="solutionsection",
            name="title_de",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="solutionsection",
            name="title_en",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="solutionsection",
            name="title_es",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="solutionsection",
            name="title_fr",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="solutionsection",
            name="title_it",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="solutionsection",
            name="title_nl",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="solutionsection",
            name="title_pt",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.CreateModel(
            name="BenefitItem",
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
                ("name", models.CharField(max_length=32)),
                ("name_en", models.CharField(max_length=32, null=True)),
                ("name_de", models.CharField(max_length=32, null=True)),
                ("name_es", models.CharField(max_length=32, null=True)),
                ("name_fr", models.CharField(max_length=32, null=True)),
                ("name_it", models.CharField(max_length=32, null=True)),
                ("name_nl", models.CharField(max_length=32, null=True)),
                ("name_pt", models.CharField(max_length=32, null=True)),
                ("description", models.TextField()),
                ("description_en", models.TextField(null=True)),
                ("description_de", models.TextField(null=True)),
                ("description_es", models.TextField(null=True)),
                ("description_fr", models.TextField(null=True)),
                ("description_it", models.TextField(null=True)),
                ("description_nl", models.TextField(null=True)),
                ("description_pt", models.TextField(null=True)),
                (
                    "section",
                    auto_prefetch.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="home.benefitssection",
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
