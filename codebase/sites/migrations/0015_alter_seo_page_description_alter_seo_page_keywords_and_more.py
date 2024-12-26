# Generated by Django 5.1.4 on 2024-12-25 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sites", "0014_remove_site_allow_translation_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="seo",
            name="page_description",
            field=models.TextField(max_length=256),
        ),
        migrations.AlterField(
            model_name="seo",
            name="page_keywords",
            field=models.TextField(max_length=128),
        ),
        migrations.AlterField(
            model_name="seo",
            name="page_title",
            field=models.CharField(max_length=64),
        ),
    ]