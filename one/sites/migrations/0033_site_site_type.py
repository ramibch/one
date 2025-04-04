# Generated by Django 5.1 on 2025-03-31 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sites", "0032_remove_site_description_el_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="site",
            name="site_type",
            field=models.CharField(
                choices=[
                    ("standard", "Standard"),
                    ("dgt", "DGT"),
                    ("english", "English quizzes"),
                ],
                default="standard",
                max_length=16,
            ),
        ),
    ]
