# Generated by Django 5.1.7 on 2025-03-26 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_user_possible_spam"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="language",
            field=models.CharField(
                choices=[
                    ("en", "English"),
                    ("de", "German"),
                    ("es", "Spanish"),
                    ("fr", "French"),
                    ("it", "Italian"),
                    ("nl", "Dutch"),
                    ("pt", "Portuguese"),
                ],
                max_length=8,
                null=True,
            ),
        ),
    ]
