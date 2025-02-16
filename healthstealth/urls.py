"""
URL configuration for healthstealth project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin  # noqa: admin is not accessed
from django.urls import path, include  # noqa: path, include are not accessed
from django.conf import settings
from django.conf.urls.static import static
from .api_urls import api_urlpatterns, admin_urlpatterns

urlpatterns = api_urlpatterns + admin_urlpatterns

urlpatterns  += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns  += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
