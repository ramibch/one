# Generated by Django 5.2.4 on 2025-07-20 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("candidates", "0035_jobapplication_email_force_send_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="candidate",
            old_name="receive_job_alerts",
            new_name="recommend_jobs",
        ),
        migrations.AddField(
            model_name="candidate",
            name="last_job_recommendation",
            field=models.DateTimeField(editable=False, null=True),
        ),
    ]
