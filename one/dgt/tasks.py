import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from huey import crontab
from huey.contrib import djhuey as huey

from .models import DgtQuestion, DgtTest


@huey.db_periodic_task(crontab(day=1))
def scrape_dgt_task_monthly():
    last_test = DgtTest.objects.last()
    start_page = 1 if last_test is None else last_test.dgt_page + 1
    host = "https://revista.dgt.es"
    for page_num in range(start_page, start_page + 3):
        questions = []
        url = f"{host}/es/test/Test-num-{page_num}.shtml"
        r = requests.get(url)
        if r.status_code != 200:
            continue
        soup = BeautifulSoup(r.text, "html.parser")
        test = DgtTest.objects.create(
            title=soup.find("h1").text, source_url=url, dgt_page=page_num
        )
        soup_qs = soup.find("section", class_="preguntas_test")
        for _, soup_q in enumerate(soup_qs.children):
            explanation = None
            if not isinstance(soup_q, Tag):
                continue
            soup_img = soup_q.find("img")
            img_alt = soup_img["alt"]
            img_src = soup_img["src"]
            title = soup_q.find("h4", class_="tit_not").text
            soup_corr = soup_q.find("div", class_="content_respuesta")
            correct_option = soup_corr.find("span", class_="opcion").text
            if len(list(soup_corr)) > 3:
                explanation = list(soup_corr)[4].text
            soup_ops = soup_q.find("ul")
            for op_index, soup_op in enumerate(soup_ops.children):
                if op_index == 1:
                    option_a = soup_op.text
                elif op_index == 3:
                    option_b = soup_op.text
                elif op_index == 5:
                    option_c = soup_op.text
            questions.append(
                DgtQuestion(
                    test=test,
                    title=title,
                    option_a=option_a,
                    option_b=option_b,
                    option_c=option_c,
                    correct_option=correct_option,
                    explanation=explanation,
                    img_alt=img_alt,
                    img_url=host + img_src,
                )
            )
        DgtQuestion.objects.bulk_create(questions)


@huey.db_periodic_task(crontab(hour="20", minute="30"))
def process_unsaved_image_of_dgt_questions():
    for q in DgtQuestion.objects.filter(image=""):
        q.save()
