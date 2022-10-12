from atexit import register
from django.contrib import admin

from .models import Blurb
from .models import Response
from .models import Bio



admin.site.register(Blurb)
admin.site.register(Response)
admin.site.register(Bio)

# Register your models here.
