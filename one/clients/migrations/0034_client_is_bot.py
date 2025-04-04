# Generated by Django 5.2 on 2025-04-03 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0033_remove_client_is_bot"),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="is_bot",
            field=models.GeneratedField(
                db_persist=True,
                expression=models.Case(
                    models.When(
                        models.Q(
                            ("user_agent__contains", "bot"),
                            ("user_agent__contains", "Bot"),
                            ("user_agent__contains", "Python"),
                            ("user_agent__contains", "AppEngine"),
                            ("user_agent__contains", "Mastodon"),
                            ("user_agent__contains", "Crawl"),
                            ("user_agent__contains", "crawl"),
                            ("user_agent__contains", "facebookexternalhit"),
                            ("user_agent__contains", "SnoopSecInspect"),
                            ("user_agent__contains", "letsencrypt.org"),
                            ("user_agent__contains", ".NET"),
                            ("user_agent__contains", "sindresorhus/got"),
                            ("user_agent__contains", "YaSearchApp"),
                            ("user_agent__contains", "Palo Alto Networks"),
                            ("user_agent__contains", "ipip.net"),
                            ("user_agent__contains", "Java"),
                            ("user_agent__contains", "HttpClient"),
                            ("user_agent__contains", "spider"),
                            ("user_agent__contains", "project-resonance.com"),
                            ("user_agent__contains", "Scanner"),
                            ("user_agent__contains", "scanner"),
                            ("user_agent__contains", "Inspect"),
                            ("user_agent__contains", "inspect"),
                            ("user_agent__contains", "Grammarly"),
                            ("user_agent__contains", "GoogleOther"),
                            _connector="OR",
                        ),
                        then=models.Value(True),
                    ),
                    default=models.Value(False),
                ),
                output_field=models.BooleanField(db_default=False),
            ),
        ),
    ]
