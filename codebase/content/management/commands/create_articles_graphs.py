import os
from itertools import chain

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = "Create pngs from gnuplot scripts (with extension .plt)"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Processing...")

        pub_path = settings.BASE_DIR / "material" / "articles"
        draft_path = settings.BASE_DIR / "material" / "drafts"

        plt_paths = chain(pub_path.rglob("*.plt"), draft_path.rglob("*.plt"))

        tex_paths = chain(pub_path.rglob("*.tex"), draft_path.rglob("*.tex"))

        for p in plt_paths:
            try:
                os.system(f"cd {str(p.parent)} && gnuplot -c {str(p)}")
                print(f"✅ {str(p)}")
            except Exception as e:
                print(f"🔴 {str(p)}. Error: {e}")
        for p in tex_paths:
            try:
                os.system(f"cd '{str(p.parent)}' && pdflatex -shell-escape '{str(p)}'")
                print(f"✅ {str(p)}")
            except Exception as e:
                print(f"🔴 {str(p)}. Error: {e}")

        self.stdout.write("Done.")
