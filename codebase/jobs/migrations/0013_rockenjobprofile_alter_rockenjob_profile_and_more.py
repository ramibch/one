# Generated by Django 4.2.5 on 2023-09-18 09:18

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("jobs", "0012_alter_rockenjobsearch_profile"),
    ]

    operations = [
        migrations.CreateModel(
            name="RockenJobProfile",
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
                ("first_name", models.CharField(max_length=32)),
                ("last_name", models.CharField(max_length=64)),
                ("email", models.CharField(max_length=64)),
                (
                    "phone_country",
                    models.CharField(
                        choices=[("es", "Spain"), ("de", "Germany")], max_length=5
                    ),
                ),
                ("phone_number", models.CharField(max_length=32)),
                (
                    "actual_position",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                ("link", models.URLField(blank=True, max_length=128, null=True)),
                (
                    "cv",
                    models.FileField(
                        storage=django.core.files.storage.FileSystemStorage(
                            base_url="/media/", location="/media/social/"
                        ),
                        upload_to="jobs",
                    ),
                ),
                (
                    "certificates",
                    models.FileField(
                        storage=django.core.files.storage.FileSystemStorage(
                            base_url="/media/", location="/media/social/"
                        ),
                        upload_to="jobs",
                    ),
                ),
                (
                    "extra_doc",
                    models.FileField(
                        blank=True,
                        null=True,
                        storage=django.core.files.storage.FileSystemStorage(
                            base_url="/media/", location="/media/social/"
                        ),
                        upload_to="jobs",
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="rockenjob",
            name="profile",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="jobs.rockenjobprofile",
            ),
        ),
        migrations.AlterField(
            model_name="rockenjobapplication",
            name="profile",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="jobs.rockenjobprofile",
            ),
        ),
        migrations.AlterField(
            model_name="rockenjobsearch",
            name="profile",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="jobs.rockenjobprofile"
            ),
        ),
        migrations.DeleteModel(
            name="Profile",
        ),
    ]