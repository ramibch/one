# Generated by Django 5.1.4 on 2024-12-26 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0014_alter_articlessection_card_animation_class"),
    ]

    operations = [
        migrations.AddField(
            model_name="herosection",
            name="cta_animation_class",
            field=models.CharField(
                blank=True,
                choices=[
                    ("bounce", "Bounce"),
                    ("flash", "Flash"),
                    ("pulse", "Pulse"),
                    ("rubberBand", "Rubber Band"),
                    ("shakeX", "Shake X"),
                    ("shakeY", "Shake Y"),
                    ("headShake", "Head Shake"),
                    ("swing", "Swing"),
                    ("tada", "Tada"),
                    ("wobble", "Wobble"),
                    ("jello", "Jello"),
                    ("heartBeat", "Heart Beat"),
                ],
                default="flash",
                max_length=16,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="herosection",
            name="cta_animation_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("vanilla", "Vanilla"),
                    ("onmouseover", "On event: onmouseover"),
                ],
                default="vanilla",
                max_length=16,
                null=True,
            ),
        ),
    ]