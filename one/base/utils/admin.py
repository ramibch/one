from django.db import models
from django.forms.widgets import CheckboxSelectMultiple

from one.base.utils.db_fields import ChoiceArrayField

FORMFIELD_OVERRIDES_DICT = {
    models.ManyToManyField: {"widget": CheckboxSelectMultiple},
    ChoiceArrayField: {"widget": CheckboxSelectMultiple},
}
