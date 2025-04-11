from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from apps.authentication.versioned_api.v1.routers import urlpatterns as authentication_urlpatterns
from apps.accounts.versioned_api.v1.routers import urlpatterns as accounts_urlpatterns
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

version = 'v1'
api_urlpatterns = [
    path(f'api/{version}/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(f'api/{version}/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path(f'api/{version}/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(f'', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path(f'api/{version}/auth/', include(authentication_urlpatterns)),
    path(f'api/{version}/accounts/', include(accounts_urlpatterns)),
]

admin_urlpatterns = [
    path('admin/', admin.site.urls),
]

