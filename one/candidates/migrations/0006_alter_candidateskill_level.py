# Generated by Django 5.2 on 2025-06-21 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("candidates", "0005_alter_candidateskill_level"),
    ]

    operations = [
        migrations.AlterField(
            model_name="candidateskill",
            name="level",
            field=models.IntegerField(
                choices=[
                    (1, "Beginner"),
                    (2, "Learner"),
                    (3, "Competent"),
                    (4, "Proficient"),
                    (5, "Expert"),
                ]
            ),
        ),
    ]
