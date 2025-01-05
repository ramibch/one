from django.contrib import admin

# Register your models here.

from .models import RockenJob
from .models import RockenJobProfile
from .models import RockenJobApplication
from .models import RockenJobSearch

admin.site.register(RockenJob)
admin.site.register(RockenJobProfile)
admin.site.register(RockenJobApplication)
admin.site.register(RockenJobSearch)
