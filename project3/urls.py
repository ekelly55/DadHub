from django.contrib import admin
from django.urls import path, include # <- you must add include to the imports

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dad_hub.urls')) # <- here is the new line to include the urls of our app
]
