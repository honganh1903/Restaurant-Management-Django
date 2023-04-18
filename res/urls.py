from django.urls import path
from .views import *
from .admin import admin_site

urlpatterns = [
    path("/", home),
    path("home/", home),
    path("add-student/", res_add),
    path('admin/', admin_site.urls),
]