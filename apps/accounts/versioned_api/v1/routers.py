from apps.accounts.views.user_registration import ResendVerificationCode, UserRegistration,EmailCodeVerification
from django.urls import path


urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user-registration'),
    path('verify-email',EmailCodeVerification.as_view(),name='verify-email'),
    path('resend-verification-code/', ResendVerificationCode.as_view(), name='resend-verification-code')
]