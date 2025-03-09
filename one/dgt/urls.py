from django.urls import path

from . import feeds, views

urlpatterns = [
    path("", views.test_index, name="test-index"),
    path("<int:id>", views.question_detail, name="question-detail"),
    path("<int:id>/check/", views.check_question, name="question-check"),
    # Feed
    path("pins/questions", feeds.DgtQuestionPinFeed()),
]
