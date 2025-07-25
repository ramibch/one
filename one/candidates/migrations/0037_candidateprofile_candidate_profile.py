# Generated by Django 5.2.4 on 2025-07-21 20:00

import auto_prefetch
import django.db.models.deletion
import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "candidates",
            "0036_rename_receive_job_alerts_candidate_recommend_jobs_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="CandidateProfile",
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
                ("title", models.CharField()),
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
            model_name="candidate",
            name="profile",
            field=auto_prefetch.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="candidates.candidateprofile",
            ),
        ),
    ]
