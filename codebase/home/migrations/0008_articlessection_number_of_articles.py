# Generated by Django 5.1.4 on 2024-12-21 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0007_rename_faq_categories_faqssection_auto_add_categories"),
    ]

    operations = [
        migrations.AddField(
            model_name="articlessection",
            name="number_of_articles",
            field=models.PositiveSmallIntegerField(default=6),
        ),
    ]