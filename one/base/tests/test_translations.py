import polib
from django.conf import settings
from django.test import TestCase
from django.utils import translation


class TestProjectTranslations(TestCase):
    def get_pofile(self, lang):
        return polib.pofile(f"{settings.BASE_DIR}/locale/{lang}/LC_MESSAGES/django.po")

    def test_translations(self):
        for lang in settings.LANGUAGE_CODES_WITHOUT_DEFAULT:
            if lang in settings.LANGUAGE_CODE or lang == settings.LANGUAGE_CODE:
                # Default language has no po file.
                continue
            with translation.override(lang):
                for entry in self.get_pofile(lang=lang):
                    out = translation.gettext(entry.msgid)
                    msg = None
                    if entry.msgstr_plural == {}:
                        self.assertEqual(out, entry.msgstr)
                        msg = entry.msgstr
                    elif 0 in entry.msgstr_plural:
                        self.assertEqual(out, entry.msgstr_plural[0])
                        msg = entry.msgstr_plural[0]
                    elif 1 in entry.msgstr_plural:
                        self.assertEqual(out, entry.msgstr_plural[1])
                        msg = entry.msgstr_plural[1]

                    if msg:
                        print(f"Original: {entry.msgid}")
                        print(f"Translation: {msg}")
