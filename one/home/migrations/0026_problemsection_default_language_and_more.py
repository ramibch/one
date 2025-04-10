# Generated by Django 5.1 on 2025-03-15 11:44

import one.base.utils.db
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0025_rename_rest_languages_articlessection_languages_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="problemsection",
            name="default_language",
            field=models.CharField(
                choices=[
                    ("en", "English"),
                    ("de", "German"),
                    ("es", "Spanish"),
                    ("fr", "French"),
                    ("el", "Greek"),
                    ("it", "Italian"),
                    ("nl", "Dutch"),
                    ("pl", "Polish"),
                    ("pt", "Portuguese"),
                    ("ru", "Russian"),
                    ("sk", "Slovak"),
                    ("sl", "Slovenian"),
                    ("sv", "Swedish"),
                    ("tr", "Turkish"),
                    ("uk", "Ukrainian"),
                ],
                default="en",
                max_length=4,
            ),
        ),
        migrations.AddField(
            model_name="problemsection",
            name="languages",
            field=one.base.utils.db.ChoiceArrayField(
                base_field=models.CharField(
                    choices=[
                        ("en", "English"),
                        ("de", "German"),
                        ("es", "Spanish"),
                        ("fr", "French"),
                        ("el", "Greek"),
                        ("it", "Italian"),
                        ("nl", "Dutch"),
                        ("pl", "Polish"),
                        ("pt", "Portuguese"),
                        ("ru", "Russian"),
                        ("sk", "Slovak"),
                        ("sl", "Slovenian"),
                        ("sv", "Swedish"),
                        ("tr", "Turkish"),
                        ("uk", "Ukrainian"),
                    ],
                    max_length=8,
                ),
                blank=True,
                default=list,
                size=None,
            ),
        ),
    ]
