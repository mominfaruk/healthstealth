from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

version = 'v1'
api_urlpatterns = [
    path(f'api/{version}/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(f'api/{version}/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
