# Generated by Django 4.2.5 on 2023-09-13 20:01

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("jobs", "0002_profile_rockenjobapplication_applied_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="actual_position",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="extra_doc",
            field=models.FileField(
                blank=True,
                null=True,
                storage=django.core.files.storage.FileSystemStorage(),
                upload_to="jobs",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="last_name",
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name="profile",
            name="link",
            field=models.URLField(blank=True, max_length=128, null=True),
        ),
    ]