# Generated by Django 5.1.4 on 2025-01-08 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0021_pathredirect_for_users_only"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="pathredirect",
            name="for_users_only",
        ),
        migrations.AddField(
            model_name="pathredirect",
            name="applicable_when",
            field=models.CharField(
                choices=[
                    ("user", "👤 Redirect for logged user"),
                    ("no_user", "🕵🏻 Redirect for anonymous user"),
                    ("always", "🔄 Always redirect"),
                ],
                default="always",
                max_length=16,
            ),
        ),
    ]
