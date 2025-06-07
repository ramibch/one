import codecs
import platform
import tempfile
from pathlib import Path
from subprocess import CalledProcessError, run

from django.template.loader import get_template

from .exceptions import TexError


def render_pdf(
    template_name: str,
    context: dict,
    interpreter: str = "pdflatex",
    interpreter_opts: str = "-interaction=batchmode -no-shell-escape",
    run_times: int = 1,
) -> tuple[bytes, str]:
    # rendering pdf file
    template = get_template(template_name, using="tex")
    rendered_text = template.render(context)
    null = "$null" if "Windows" in platform.system() else "/dev/null"
    filename = "texput.tex"
    with tempfile.TemporaryDirectory() as tempdir:
        temppath = Path(tempdir)
        with open(temppath / filename, "x", encoding="utf-8") as f:
            f.write(rendered_text)
        args = f"{interpreter} {interpreter_opts} {filename} 2>&1 > {null}"
        try:
            for _ in range(run_times):
                run(args, shell=True, capture_output=True, check=True, cwd=tempdir)
        except CalledProcessError as called_process_error:
            try:
                # with open(temppath / "texput.log", encoding="utf-8") as f:
                with codecs.open(
                    temppath / "texput.log", "r", encoding="utf-8", errors="ignore"
                ) as f:
                    log = f.read()
            except FileNotFoundError:
                raise called_process_error  # noqa: B904
            else:
                raise TexError(
                    log=log, source=rendered_text, template_name=template_name
                )
        with open(temppath / "texput.pdf", "rb") as f:
            bytes_pdf = f.read()

        return bytes_pdf, rendered_text
