# Generated by Django 5.1.4 on 2024-12-26 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "home",
            "0016_rename_card_animation_class_articlessection_card_animation_name_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="articlessection",
            name="card_animation_repeat",
            field=models.CharField(
                blank=True,
                choices=[
                    ("1", "1 Time"),
                    ("2", "2 Times"),
                    ("3", "3 Times"),
                    ("infinite", "Infinite times"),
                ],
                default="infinite",
                max_length=16,
                null=True,
            ),
        ),
    ]