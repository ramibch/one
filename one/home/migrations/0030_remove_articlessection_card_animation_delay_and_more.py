# Generated by Django 5.1.7 on 2025-03-21 23:26

import auto_prefetch
import django.db.models.deletion
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        # ("animations", "__first__"),
        ("home", "0029_remove_home_benefits_title_remove_home_steps_title"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="articlessection",
            name="card_animation_delay",
        ),
        migrations.RemoveField(
            model_name="articlessection",
            name="card_animation_name",
        ),
        migrations.RemoveField(
            model_name="articlessection",
            name="card_animation_repeat",
        ),
        migrations.RemoveField(
            model_name="articlessection",
            name="card_animation_speed",
        ),
        migrations.RemoveField(
            model_name="articlessection",
            name="card_animation_type",
        ),
        migrations.RemoveField(
            model_name="herosection",
            name="cta_animation_delay",
        ),
        migrations.RemoveField(
            model_name="herosection",
            name="cta_animation_name",
        ),
        migrations.RemoveField(
            model_name="herosection",
            name="cta_animation_repeat",
        ),
        migrations.RemoveField(
            model_name="herosection",
            name="cta_animation_speed",
        ),
        migrations.RemoveField(
            model_name="herosection",
            name="cta_animation_type",
        ),
        migrations.AddField(
            model_name="articlessection",
            name="card_animation",
            field=auto_prefetch.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="animations.animation",
            ),
        ),
        migrations.AddField(
            model_name="herosection",
            name="cta_animation",
            field=auto_prefetch.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="animations.animation",
            ),
        ),
    ]
