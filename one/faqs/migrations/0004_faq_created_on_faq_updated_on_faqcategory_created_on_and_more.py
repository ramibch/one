# Generated by Django 5.2 on 2025-05-21 19:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("faqs", "0003_faq_categories"),
    ]

    operations = [
        migrations.AddField(
            model_name="faq",
            name="created_on",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 15, 21, 560060, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AddField(
            model_name="faq",
            name="updated_on",
            field=models.DateTimeField(
                auto_now=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 15, 21, 560114, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AddField(
            model_name="faqcategory",
            name="created_on",
            field=models.DateTimeField(
                auto_now_add=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 15, 21, 560060, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
        migrations.AddField(
            model_name="faqcategory",
            name="updated_on",
            field=models.DateTimeField(
                auto_now=True,
                db_default=datetime.datetime(
                    2025, 5, 21, 19, 15, 21, 560114, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
    ]
