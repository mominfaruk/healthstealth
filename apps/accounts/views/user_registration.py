from datetime import timedelta
import random
import string
import jwt

from django.utils import timezone
from django.conf import settings
from rest_framework import generics
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from apps.gist.views.logger import LogHelper
from apps.gist.views.email import EmailService
from apps.accounts.serializers.users_serializer import UserRegisterSerializer
from apps.accounts.models.users import User
from apps.accounts.models.verification_code import VerificationCode
from healthstealth.configs.email_template_settings import EMAIL_TEMPLATES


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
            current_time = timezone.now()
            expiry_time = current_time + timedelta(minutes=15)
            
            verification_code_obj, created = VerificationCode.objects.update_or_create(
                user=instance,
                defaults={
                    'email_verification_code': verification_code,
                    'email_verification_code_last_sent': current_time,
                    'email_verification_code_expiry': expiry_time
                }
            )
            
            verification_token = jwt.encode({
                'user_id': instance.id,
                'verification_code': verification_code,
                'exp': expiry_time
            }, settings.SECRET_KEY, algorithm='HS256')
            
            context = {
                'verification_token': verification_token,
                'verification_code': verification_code,
            }
            EmailService().send_email(
                recipients=[instance.email],
                context=context,
                subject="Please Verify Your Email Address",
                template_name=EMAIL_TEMPLATES.get('user_registration_verification'),
                from_email=settings.DEFAULT_FROM_EMAIL,
                email_type="verification"
            )
            
        except Exception as e:
            LogHelper.fail_log(e)
            raise e
        
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {"success": False, "error": serializer.errors},
                    status=400
                )
            self.perform_create(serializer)
            return Response(
                {"success": True, "message": "User created successfully"},
                status=201
            )
        except Exception as e:
            LogHelper.fail_log(e)
            return Response(
                {"success": False, "message": "An error occurred during registration"},
                status=500
            )
    
    def generate_verification_code(self):
        return ''.join(random.choices(string.digits, k=6))