# Generated by Django 5.2 on 2025-05-21 19:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("etsy", "0004_alter_app_created_on_alter_app_updated_on_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="app",
            name="created_on",
        ),
        migrations.RemoveField(
            model_name="app",
            name="updated_on",
        ),
        migrations.RemoveField(
            model_name="etsyauth",
            name="created_on",
        ),
        migrations.RemoveField(
            model_name="etsyauth",
            name="updated_on",
        ),
        migrations.RemoveField(
            model_name="listing",
            name="created_on",
        ),
        migrations.RemoveField(
            model_name="listing",
            name="updated_on",
        ),
        migrations.RemoveField(
            model_name="listingfile",
            name="created_on",
        ),
        migrations.RemoveField(
            model_name="listingfile",
            name="updated_on",
        ),
        migrations.RemoveField(
            model_name="listingimage",
            name="created_on",
        ),
        migrations.RemoveField(
            model_name="listingimage",
            name="updated_on",
        ),
        migrations.RemoveField(
            model_name="shop",
            name="created_on",
        ),
        migrations.RemoveField(
            model_name="shop",
            name="updated_on",
        ),
        migrations.AddField(
            model_name="app",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 18, 53, 848231, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AddField(
            model_name="app",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 18, 53, 848323, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AddField(
            model_name="etsyauth",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 18, 53, 848231, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AddField(
            model_name="etsyauth",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 18, 53, 848323, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AddField(
            model_name="listing",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 18, 53, 848231, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AddField(
            model_name="listing",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 18, 53, 848323, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AddField(
            model_name="listingfile",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 18, 53, 848231, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AddField(
            model_name="listingfile",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 18, 53, 848323, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AddField(
            model_name="listingimage",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 18, 53, 848231, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AddField(
            model_name="listingimage",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 18, 53, 848323, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AddField(
            model_name="shop",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 18, 53, 848231, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AddField(
            model_name="shop",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 18, 53, 848323, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
    ]
