from django.urls import re_path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    re_path(r'', include(('res.urls', 'res'), namespace='res')),
    re_path(r'^res/', include('res.urls')),
    re_path(r'^admin/', admin.site.urls),
]