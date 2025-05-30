# Generated by Django 5.2 on 2025-05-21 19:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0004_articlefile_created_on_articlefile_updated_on_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="created_on",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 17, 9, 777148, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AlterField(
            model_name="article",
            name="updated_on",
            field=models.DateTimeField(
                auto_now=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 17, 9, 777236, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AlterField(
            model_name="articlefile",
            name="created_on",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 17, 9, 777148, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AlterField(
            model_name="articlefile",
            name="updated_on",
            field=models.DateTimeField(
                auto_now=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 17, 9, 777236, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="created_on",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 17, 9, 777148, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="updated_on",
            field=models.DateTimeField(
                auto_now=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 17, 9, 777236, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AlterField(
            model_name="maintopic",
            name="created_on",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 17, 9, 777148, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AlterField(
            model_name="maintopic",
            name="updated_on",
            field=models.DateTimeField(
                auto_now=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 17, 9, 777236, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
    ]
