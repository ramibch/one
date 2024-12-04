# Generated by Django 5.1.3 on 2024-11-23 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0012_remove_language_code_alter_extendedsite_language_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="extendedsite",
            name="default_page_description_fr",
            field=models.TextField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name="extendedsite",
            name="default_page_keywords_fr",
            field=models.TextField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name="extendedsite",
            name="default_page_title_fr",
            field=models.CharField(max_length=64, null=True),
        ),
    ]