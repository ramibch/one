# Generated by Django 5.1 on 2025-03-28 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("emails", "0028_alter_postalmessage_sent_with_ssl"),
    ]

    operations = [
        migrations.AddField(
            model_name="sender",
            name="domain_validation",
            field=models.BooleanField(default=True),
        ),
    ]
