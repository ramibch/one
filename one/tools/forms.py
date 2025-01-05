from django import forms


class GnuplotSpider(forms.Form):
    data = forms.Textarea()


class SeoCheckForm(forms.Form):
    site = forms.URLField()
