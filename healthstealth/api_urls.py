from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from apps.authentication.versioned_api.v1.routers import urlpatterns as authentication_urlpatterns

version = 'v1'
api_urlpatterns = [
    path(f'api/{version}/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(f'api/{version}/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path(f'api/{version}/auth/', include(authentication_urlpatterns)),
]

admin_urlpatterns = [
    path('admin/', admin.site.urls),
]
