# Generated by Django 5.1.4 on 2024-12-26 02:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0015_herosection_cta_animation_class_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="articlessection",
            old_name="card_animation_class",
            new_name="card_animation_name",
        ),
        migrations.RenameField(
            model_name="herosection",
            old_name="cta_animation_class",
            new_name="cta_animation_name",
        ),
    ]
