# Generated by Django 5.2 on 2025-04-14 21:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("links", "0016_alter_link_topic"),
    ]

    operations = [
        migrations.RenameField(
            model_name="link",
            old_name="django_url_path",
            new_name="url_path",
        ),
        migrations.RemoveField(
            model_name="link",
            name="article",
        ),
        migrations.RemoveField(
            model_name="link",
            name="plan",
        ),
    ]
