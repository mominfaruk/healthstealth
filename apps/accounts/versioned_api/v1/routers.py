from apps.accounts.views.user_registration import UserRegistration
from django.urls import path


urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user-registration'),
]