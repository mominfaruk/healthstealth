from datetime import timedelta
import random
import string
import jwt

from django.utils import timezone
from django.conf import settings
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
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
            email=request.data.get('email')
            exiting_user=User.objects.filter(email=email).exists()
            if exiting_user:
                verification_status=exiting_user.verificationcode_set.filter(email_verified=False).first()
                if verification_status:

                    current_time = timezone.now()
                    if verification_status.email_verification_code_expiry > current_time:
                        return Response(
                            {"success": False, "message": "Email already registered and verification code sent"},
                            status=400
                        )
                else:
                    return Response(
                        {"success": False, "message": "Email already registered"},
                        status=400
                    )                                                                         
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


class EmailVerificationThrottle(AnonRateThrottle):
    rate='10/minute'
    scope='email_code_verification'
@extend_schema(
    description="This api is for verifying the code for user registration",
    request={
        'application/json':{
            'type':'object',
            'properties':{
                'email':{'type':'string','format':'email'},
                'verification_code':{'type':'string', 'example':'10234'}
            },
            'required':['email','verification_code']
        }
    },
    responses={
        200:OpenApiResponse(description="code verified successfully"),
        400:OpenApiResponse(description="Bad request")
    }
)
class EmailCodeVerification(generics.GenericAPIView):
    permission_classes=[]
    throttle_classes=[EmailVerificationThrottle]

    def post(self,request, *args, **kwargs):
        email=request.data.get('email')
        verification_code=request.data.get('verification_code')
        print(email,verification_code)
        user=User.objects.filter(email=email).first()
        if not user:
            return Response({"success":False, "message":"User not found"},status=400)
        user_verification_code=user.verificationcode_set.filter(email_verification_code_expiry__gt=timezone.now(),email_verified=False).first()
        if not user_verification_code:
            return Response({"success": False, "message": "Expired verification code  or email is already verified"}, status=400)
        if verification_code==user_verification_code.email_verification_code:
            user_verification_code.email_verified=True
            user_verification_code.save()
            return Response({'success': True, 'message': 'Email verified successfully'},status=200)
        return Response({"success": False, "message":"Code verification failed"},status=400)


@extend_schema(
    description="This api is for resending the verification code for user registration",
    request={
        'application/json':{
            'type':'object',
            'properties':{
                'email' : {'type': 'string', 'format': 'email'}
            }
        }
    }
)                                                 
class ResendVerificationCode(generics.GenericAPIView):
    permission_classes = []
    

    def post(self,request, *args, **kwargs):
        email = request.data.get('email')
        user=User.objects.filter(email=email).first()

        if user.verificationcode_set.filter(email_verified=True).exists():
            return Response({"success": False, "message": "Email does not exist or already verified"}, status=400)

        if not user:
            return Response({"success": False, "message": "User not found"}, status=400)
        current_time = timezone.now()
        verification_code = UserRegistration().generate_verification_code()
        expiry_time = current_time + timedelta(minutes=15)
        verification_code_obj, created = VerificationCode.objects.update_or_create(
            user=user,
            defaults={
                'email_verification_code': verification_code,
                'email_verification_code_last_sent': current_time,
                'email_verification_code_expiry': expiry_time
            }
        )
        verification_code=jwt.encode({
            'user_id': user.id,
            'verification_code': verification_code,
            'exp': expiry_time
        }, settings.SECRET_KEY, algorithm='HS256')
        
        context = {
            'verification_token': verification_code,
            'verification_code': verification_code,
        }
        EmailService().send_email(
            recipients=[user.email],
            context=context,
            subject="Your Verification Code",
            template_name=EMAIL_TEMPLATES.get('resend_verification_code'),
            from_email=settings.DEFAULT_FROM_EMAIL,
            email_type="verification"
        )
        return Response({"success": True, "message": "Verification code resent successfully"}, status=200)