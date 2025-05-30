# Generated by Django 5.2 on 2025-05-21 19:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "companies",
            "0012_alter_company_created_on_alter_company_updated_on_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="company",
            name="created_on",
        ),
        migrations.RemoveField(
            model_name="company",
            name="updated_on",
        ),
        migrations.RemoveField(
            model_name="companylocation",
            name="created_on",
        ),
        migrations.RemoveField(
            model_name="companylocation",
            name="updated_on",
        ),
        migrations.RemoveField(
            model_name="job",
            name="created_on",
        ),
        migrations.RemoveField(
            model_name="job",
            name="updated_on",
        ),
        migrations.RemoveField(
            model_name="person",
            name="created_on",
        ),
        migrations.RemoveField(
            model_name="person",
            name="updated_on",
        ),
        migrations.AddField(
            model_name="company",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 18, 53, 848231, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AddField(
            model_name="company",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 18, 53, 848323, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AddField(
            model_name="companylocation",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 18, 53, 848231, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AddField(
            model_name="companylocation",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 18, 53, 848323, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AddField(
            model_name="job",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 18, 53, 848231, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AddField(
            model_name="job",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 18, 53, 848323, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AddField(
            model_name="person",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 18, 53, 848231, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AddField(
            model_name="person",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 18, 53, 848323, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
    ]
