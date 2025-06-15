# evaluation/urls.py

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from web.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
]

# DEBUG 모드에서 media 파일(보고서 PNG 등) 서빙
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
