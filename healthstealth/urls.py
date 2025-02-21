from django.contrib import admin  # noqa: admin is not accessed
from django.urls import path, include  # noqa: path, include are not accessed
from django.conf import settings
from django.conf.urls.static import static
from .api_urls import api_urlpatterns, admin_urlpatterns

urlpatterns = api_urlpatterns + admin_urlpatterns
urlpatterns  += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns  += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
