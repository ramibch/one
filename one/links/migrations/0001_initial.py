# Generated by Django 5.2 on 2025-04-26 09:29

import django.db.models.manager
import one.db
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Link",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "language",
                    models.CharField(
                        choices=[
                            ("en", "English"),
                            ("de", "German"),
                            ("es", "Spanish"),
                            ("fr", "French"),
                            ("it", "Italian"),
                            ("nl", "Dutch"),
                            ("pt", "Portuguese"),
                        ],
                        default="en",
                        max_length=4,
                    ),
                ),
                (
                    "languages",
                    one.db.ChoiceArrayField(
                        base_field=models.CharField(
                            choices=[
                                ("en", "English"),
                                ("de", "German"),
                                ("es", "Spanish"),
                                ("fr", "French"),
                                ("it", "Italian"),
                                ("nl", "Dutch"),
                                ("pt", "Portuguese"),
                            ],
                            max_length=8,
                        ),
                        blank=True,
                        default=list,
                        size=None,
                    ),
                ),
                (
                    "custom_title",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
                (
                    "custom_title_en",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
                (
                    "custom_title_de",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
                (
                    "custom_title_es",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
                (
                    "custom_title_fr",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
                (
                    "custom_title_it",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
                (
                    "custom_title_nl",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
                (
                    "custom_title_pt",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
                (
                    "external_url",
                    models.URLField(blank=True, max_length=256, null=True),
                ),
                (
                    "url_path",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("home", "Home"),
                            ("search", "Search"),
                            ("sitemap", "Sitemap"),
                            ("contact", "Contact"),
                            ("article_list", "Articles"),
                            ("plan_list", "Plans"),
                            ("account_login", "Sign In"),
                            ("account_signup", "Sign Up"),
                            ("user_dashboard", "Account"),
                            ("faq_list", "FAQs"),
                            ("quiz_list", "English Quizzes"),
                            ("privacy", "Privacy Policy"),
                            ("terms", "Terms and Conditions"),
                            ("impress", "Impress"),
                        ],
                        max_length=32,
                        null=True,
                    ),
                ),
                (
                    "topic",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("django", "Django"),
                            ("htmx", "htmx"),
                            ("alpinejs", "AlpineJS"),
                            ("devops", "DevOps"),
                            ("python", "Python"),
                            ("linux", "Linux"),
                            ("latex", "LaTex"),
                            ("matlab", "Matlab"),
                            ("siemens", "Siemens"),
                            ("excel", "Excel"),
                            ("maths", "Maths"),
                            ("mechanics", "Mechanics"),
                            ("english", "English"),
                            ("electronics", "Electronics"),
                            ("calendar", "Calendars"),
                        ],
                        max_length=16,
                        null=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
                "base_manager_name": "prefetch_manager",
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
        ),
    ]
