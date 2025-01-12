from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from .models import DgtQuestion, DgtTest, SessionDgtQuestion, SessionDgtTest


def test_index(request):
    context = {"tests": DgtTest.objects.all(), "page_title": "DGT tests anteriores"}
    return render(request, "dgt/index.html", context)


def question_detail(request, id):
    obj = get_object_or_404(DgtQuestion, id=id)
    return render(request, "dgt/question.html", {"object": obj})


@csrf_exempt
def check_question(request, id):
    question = DgtQuestion.objects.get(id=id)
    SessionDgtQuestion.objects.create(
        question=question,
        session=request.db_session,
        selected_option=request.POST.get("selected_option", ""),
        test=question.test,
    )
    context = {"question": question}

    if request.method == "GET":
        return redirect(question.detail_url)

    next_or_done = "next" if question.has_next else "done"
    if not question.has_next:
        session_test = SessionDgtTest.objects.create(
            session=request.db_session, test=question.test
        )
        session_questions = SessionDgtQuestion.objects.filter(
            test=question.test,
            session=request.db_session,
            session_test__isnull=True,
        )
        session_questions.update(session_test=session_test)
        context["session_test"] = session_test
        context["tests"] = DgtTest.objects.all()

    return render(request, f"dgt/{next_or_done}.html", context)
