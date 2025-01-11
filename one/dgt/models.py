import auto_prefetch
from django.contrib.sessions.models import Session
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property


class DgtTest(models.Model):
    source_url = models.URLField(max_length=128)
    title = models.CharField(max_length=128)
    dgt_page = models.PositiveSmallIntegerField(null=True, blank=True)

    @cached_property
    def start_url(self):
        return self.first_question.detail_url

    @cached_property
    def first_question(self):
        return self.dgtquestion_set.first()


class DgtQuestion(auto_prefetch.Model):
    test = auto_prefetch.ForeignKey(DgtTest, null=True, on_delete=models.CASCADE)
    title = models.TextField(max_length=512)
    option_a = models.CharField(max_length=512)
    option_b = models.CharField(max_length=512)
    option_c = models.CharField(max_length=512)
    correct_option = models.CharField(max_length=1)
    explanation = models.TextField(max_length=512, null=True)
    img_alt = models.CharField(max_length=256, null=True)
    img_url = models.URLField(max_length=256)

    @cached_property
    def detail_url(self):
        return reverse("question-detail", kwargs={"id": self.id})

    @cached_property
    def check_url(self):
        return reverse("question-check", kwargs={"id": self.id})

    @cached_property
    def next_question(self):
        try:
            return DgtQuestion.objects.get(id=self.id + 1, test=self.test)
        except DgtQuestion.DoesNotExist:
            return None

    @cached_property
    def has_next(self):
        return self.next_question is not None

    @cached_property
    def next_question_url(self):
        if self.has_next:
            return self.next_question.detail_url

    @cached_property
    def previous_question(self):
        try:
            return DgtQuestion.objects.get(id=self.id - 1, test=self.test)
        except DgtQuestion.DoesNotExist:
            return None

    @cached_property
    def has_previous(self):
        return self.previous_question is not None

    @cached_property
    def previous_question_url(self):
        if self.has_previous:
            return self.previous_question.detail_url


class SessionDgtTest(auto_prefetch.Model):
    session = auto_prefetch.ForeignKey(Session, on_delete=models.CASCADE)
    test = auto_prefetch.ForeignKey(DgtTest, on_delete=models.CASCADE, null=True)

    @cached_property
    def correct_number(self):
        return self.sessiondgtquestion_set.filter(
            is_correct=True, test=self.test, session_test=self
        ).count()

    @cached_property
    def incorrect_number(self):
        return self.sessiondgtquestion_set.filter(
            is_correct=False,
            test=self.test,
            session_test=self,
        ).count()

    @cached_property
    def percentage_passed(self):
        try:
            return int(
                self.correct_number
                * 100
                / (self.correct_number + self.incorrect_number)
            )
        except ZeroDivisionError:
            return -1

    @cached_property
    def passed_emoji(self):
        return "🟢" if self.percentage_passed > 90 else "🔴"

    @cached_property
    def question_list_emojis(self):
        return "".join(
            q.correct_emoji
            for q in self.sessionquestion_set.filter(session_test=self, test=self.test)
        )


class SessionDgtQuestion(auto_prefetch.Model):
    session = auto_prefetch.ForeignKey(Session, on_delete=models.CASCADE)
    question = auto_prefetch.ForeignKey(DgtQuestion, on_delete=models.CASCADE)
    session_test = auto_prefetch.ForeignKey(
        SessionDgtTest, on_delete=models.CASCADE, null=True
    )
    test = auto_prefetch.ForeignKey(DgtTest, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1)
    is_correct = models.BooleanField(default=False)

    @cached_property
    def correct_emoji(self):
        return "🟢" if self.is_correct else "🔴"

    def option_x_emoji(self, x=""):
        if not self.is_correct and self.selected_option == x:
            return "❌"
        if self.question.correct_option == x:
            return "✅"
        return ""

    @cached_property
    def option_a_emoji(self):
        return self.option_x_emoji("a")

    @cached_property
    def option_b_emoji(self):
        return self.option_x_emoji("b")

    @cached_property
    def option_c_emoji(self):
        return self.option_x_emoji("c")

    def save(self, *args, **kwargs):
        self.is_correct = self.selected_option == self.question.correct_option
        super().save(*args, **kwargs)
