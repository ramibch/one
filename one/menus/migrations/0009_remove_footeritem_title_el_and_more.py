# Generated by Django 5.1.7 on 2025-03-26 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("menus", "0008_remove_footeritem_default_language_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="footeritem",
            name="title_el",
        ),
        migrations.RemoveField(
            model_name="footeritem",
            name="title_pl",
        ),
        migrations.RemoveField(
            model_name="footeritem",
            name="title_ru",
        ),
        migrations.RemoveField(
            model_name="footeritem",
            name="title_sk",
        ),
        migrations.RemoveField(
            model_name="footeritem",
            name="title_sl",
        ),
        migrations.RemoveField(
            model_name="footeritem",
            name="title_sv",
        ),
        migrations.RemoveField(
            model_name="footeritem",
            name="title_tr",
        ),
        migrations.RemoveField(
            model_name="footeritem",
            name="title_uk",
        ),
    ]
