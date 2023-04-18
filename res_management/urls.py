from django.contrib import admin
from django.urls import path, include
from res.admin import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    path('res/', include('res.urls')),
]
