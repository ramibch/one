# Generated by Django 5.1.4 on 2024-12-21 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0005_alter_article_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="featured",
            field=models.BooleanField(default=False),
        ),
    ]
