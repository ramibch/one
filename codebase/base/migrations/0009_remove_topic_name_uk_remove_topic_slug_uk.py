# Generated by Django 5.1.4 on 2024-12-09 22:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0008_remove_topic_name_pt_br_remove_topic_slug_pt_br"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="topic",
            name="name_uk",
        ),
        migrations.RemoveField(
            model_name="topic",
            name="slug_uk",
        ),
    ]