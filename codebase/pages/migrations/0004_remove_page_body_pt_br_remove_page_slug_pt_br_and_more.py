# Generated by Django 5.1.4 on 2024-12-09 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0003_remove_page_body_eo_remove_page_body_fi_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="page",
            name="body_pt_br",
        ),
        migrations.RemoveField(
            model_name="page",
            name="slug_pt_br",
        ),
        migrations.RemoveField(
            model_name="page",
            name="title_pt_br",
        ),
    ]