# Generated by Django 5.1.7 on 2025-03-26 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("plans", "0005_remove_plan_slug_remove_plan_slug_de_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="plan",
            name="description_el",
        ),
        migrations.RemoveField(
            model_name="plan",
            name="description_pl",
        ),
        migrations.RemoveField(
            model_name="plan",
            name="description_ru",
        ),
        migrations.RemoveField(
            model_name="plan",
            name="description_sk",
        ),
        migrations.RemoveField(
            model_name="plan",
            name="description_sl",
        ),
        migrations.RemoveField(
            model_name="plan",
            name="description_sv",
        ),
        migrations.RemoveField(
            model_name="plan",
            name="description_tr",
        ),
        migrations.RemoveField(
            model_name="plan",
            name="description_uk",
        ),
        migrations.RemoveField(
            model_name="plan",
            name="title_el",
        ),
        migrations.RemoveField(
            model_name="plan",
            name="title_pl",
        ),
        migrations.RemoveField(
            model_name="plan",
            name="title_ru",
        ),
        migrations.RemoveField(
            model_name="plan",
            name="title_sk",
        ),
        migrations.RemoveField(
            model_name="plan",
            name="title_sl",
        ),
        migrations.RemoveField(
            model_name="plan",
            name="title_sv",
        ),
        migrations.RemoveField(
            model_name="plan",
            name="title_tr",
        ),
        migrations.RemoveField(
            model_name="plan",
            name="title_uk",
        ),
    ]
