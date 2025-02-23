from datetime import datetime, timedelta
import random
import string
import jwt

from django.conf import settings
from rest_framework import generics
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from apps.gist.views.logger import LogHelper
from apps.gist.views.email import EmailService
from apps.accounts.serializers.users_serializer import UserRegisterSerializer
from apps.accounts.models.users import User
from apps.accounts.models.verification_code import VerificationCode


@extend_schema(
    description="This endpoint allows you to register a new user.",
    responses={
        201: UserRegisterSerializer,
        400: OpenApiResponse(description="Bad request"),
    }
)
class UserRegistration(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = []

    def perform_create(self, serializer):
        try:
            instance = serializer.save()
            verification_code = self.generate_verification_code()
            verification_code_obj, created = VerificationCode.objects.update_or_create(
                user=instance, 
                email_verification_code=verification_code,
                email_verification_code_last_sent=datetime.now()
            )   
            verification_code_obj.save()
            print(verification_code)
            
            '''verification token is generated using the user's ID, the verification code, and an expiry time of 15 minutes.'''
            verification_token = jwt.encode({
                'user_id': instance.id,
                'verification_code': verification_code,
                'exp': datetime.now() + timedelta(minutes=15)
            }, settings.SECRET_KEY, algorithm='HS256')
            print(verification_token)
            # Optionally, send the token via email using your EmailService
            EmailService.send_verification_email(instance.email, verification_token)

        except Exception as e:
            LogHelper.fail_log(e)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"success": True, "message": "User created successfully"}, status=201)
    
    def generate_verification_code(self):
        return ''.join(random.choices(string.digits, k=6))