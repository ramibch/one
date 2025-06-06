# Generated by Django 5.2 on 2025-05-21 19:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("landing", "0005_articlessection_created_on_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="articlessection",
            name="created_on",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 17, 9, 777148, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AlterField(
            model_name="articlessection",
            name="updated_on",
            field=models.DateTimeField(
                auto_now=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 17, 9, 777236, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AlterField(
            model_name="benefititem",
            name="created_on",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 17, 9, 777148, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AlterField(
            model_name="benefititem",
            name="updated_on",
            field=models.DateTimeField(
                auto_now=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 17, 9, 777236, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AlterField(
            model_name="faqssection",
            name="created_on",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 17, 9, 777148, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AlterField(
            model_name="faqssection",
            name="updated_on",
            field=models.DateTimeField(
                auto_now=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 17, 9, 777236, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AlterField(
            model_name="finalctasection",
            name="created_on",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 17, 9, 777148, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AlterField(
            model_name="finalctasection",
            name="updated_on",
            field=models.DateTimeField(
                auto_now=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 17, 9, 777236, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AlterField(
            model_name="herosection",
            name="created_on",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 17, 9, 777148, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AlterField(
            model_name="herosection",
            name="updated_on",
            field=models.DateTimeField(
                auto_now=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 17, 9, 777236, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AlterField(
            model_name="landingpage",
            name="created_on",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 17, 9, 777148, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AlterField(
            model_name="landingpage",
            name="updated_on",
            field=models.DateTimeField(
                auto_now=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 17, 9, 777236, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AlterField(
            model_name="problemsection",
            name="created_on",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 17, 9, 777148, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AlterField(
            model_name="problemsection",
            name="updated_on",
            field=models.DateTimeField(
                auto_now=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 17, 9, 777236, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AlterField(
            model_name="solutionsection",
            name="created_on",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 17, 9, 777148, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AlterField(
            model_name="solutionsection",
            name="updated_on",
            field=models.DateTimeField(
                auto_now=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 17, 9, 777236, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AlterField(
            model_name="stepactionsection",
            name="created_on",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 17, 9, 777148, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AlterField(
            model_name="stepactionsection",
            name="updated_on",
            field=models.DateTimeField(
                auto_now=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 17, 9, 777236, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
    ]
