# Generated by Django 5.2 on 2025-06-07 18:31

import one.candidates.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("candidates", "0004_jobapplication_coverletter_latex_text"),
    ]

    operations = [
        migrations.RenameField(
            model_name="jobapplication",
            old_name="coverletter_latex_text",
            new_name="coverletter_text",
        ),
        migrations.AddField(
            model_name="jobapplication",
            name="dossier",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=one.candidates.models.JobApplication.get_upload_path,
            ),
        ),
        migrations.AddField(
            model_name="jobapplication",
            name="dossier_text",
            field=models.TextField(blank=True, null=True),
        ),
    ]
