# Generated by Django 5.1.4 on 2024-12-09 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sites", "0007_site_page_description_uk_site_page_keywords_uk_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="site",
            name="name",
            field=models.CharField(
                max_length=50, unique=True, verbose_name="display name"
            ),
        ),
    ]