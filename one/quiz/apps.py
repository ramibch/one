from __future__ import annotations

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class QuizConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "one.quiz"
    verbose_name = _("English quizzes")
