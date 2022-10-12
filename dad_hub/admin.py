from atexit import register
from django.contrib import admin

from .models import Blurb
from .models import Response



admin.site.register(Blurb)
admin.site.register(Response)

# Register your models here.
