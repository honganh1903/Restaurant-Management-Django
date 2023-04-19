from django.contrib import admin
from django.urls import path, include
from django.urls import re_path

from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from res import views
urlpatterns = [
    re_path(r'', include(('res.urls', 'res'), namespace='res')),
    re_path(r'^res/', include('res.urls')),
    re_path(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)