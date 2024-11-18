from django.db import models
from django.forms.widgets import CheckboxSelectMultiple

FORMFIELD_OVERRIDES_DICT = {
    models.ManyToManyField: {"widget": CheckboxSelectMultiple},
}
