# Generated by Django 5.2.4 on 2025-07-31 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("emails", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="postalmessage",
            name="message_id",
            field=models.PositiveBigIntegerField(unique=True),
        ),
    ]
