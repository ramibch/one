# Generated by Django 5.1.4 on 2025-01-19 20:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("emails", "0016_remove_messagesent_message_subject_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="messagesent",
            old_name="message_direction",
            new_name="direction",
        ),
        migrations.RenameField(
            model_name="messagesent",
            old_name="message_id",
            new_name="large_id",
        ),
        migrations.RenameField(
            model_name="messagesent",
            old_name="message_from",
            new_name="mail_from",
        ),
        migrations.RenameField(
            model_name="messagesent",
            old_name="message_to",
            new_name="mail_to",
        ),
        migrations.RenameField(
            model_name="messagesent",
            old_name="message_spam_status",
            new_name="spam_status",
        ),
        migrations.RenameField(
            model_name="messagesent",
            old_name="message_tag",
            new_name="tag",
        ),
        migrations.RenameField(
            model_name="messagesent",
            old_name="message_token",
            new_name="token",
        ),
    ]
