# Generated by Django 5.1.4 on 2024-12-22 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="deleted",
            field=models.BooleanField(default=False),
        ),
    ]