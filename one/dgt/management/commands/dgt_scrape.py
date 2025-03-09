import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from django.core.management.base import BaseCommand
from django.utils import timezone

from ...models import DgtQuestion, DgtTest


class Command(BaseCommand):
    help = "Creates initial objects for the site"

    def handle(self, *args, **options):
        self.stdout.write("Creating objects...")
        host = "https://revista.dgt.es"
        for i in range(241, 269):  # 269
            questions = []
            url = f"{host}/es/test/Test-num-{i}.shtml"
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            test = DgtTest.objects.create(
                title=soup.find("h1").text,
                source_url=url,
                scrapped_on=timezone.now(),
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
