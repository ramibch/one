# Generated by Django 5.1.4 on 2025-01-26 09:01

from django.db import migrations, models

import one.base.utils.db


class Migration(migrations.Migration):

    dependencies = [
        ("faqs", "0005_remove_faq_is_active"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="faq",
            name="allow_translation",
        ),
        migrations.RemoveField(
            model_name="faq",
            name="override_translated_fields",
        ),
        migrations.AddField(
            model_name="faq",
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
            model_name="faq",
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
                    max_length=4,
                ),
                blank=True,
                default=list,
                size=None,
            ),
        ),
    ]
