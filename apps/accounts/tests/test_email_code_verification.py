from django.test import TestCase, override_settings
from rest_framework.test import APIRequestFactory
from django.utils import timezone
from datetime import timedelta
from apps.accounts.models.verification_code import VerificationCode
from apps.accounts.models.users import User
from apps.accounts.views.user_registration import EmailCodeVerification

@override_settings(SECRET_KEY='test_secret_key')
class EmailCodeVerificationTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = EmailCodeVerification.as_view()

        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='StrongPass123!'
        )
        self.verification_code = '123456'
        self.verification_code_obj = VerificationCode.objects.create(
            user=self.user,
            email_verification_code=self.verification_code,
            email_verification_code_last_sent=timezone.now(),
            email_verification_code_expiry=timezone.now() + timedelta(minutes=15),
        )

    
    def test_successful_verification(self):
        request_data= {
            'verification_code': self.verification_code,
            'email': self.user.email
        }
        request = self.factory.post('/api/v1/verify-email', request_data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'success': True, 'message': 'Email verified successfully'})

        self.verification_code_obj.refresh_from_db()
        self.assertTrue(self.verification_code_obj.email_verified)


    def test_invalid_verification_code(self):
        request_data={
            'verification_coe':99999,
            'email':self.user.email
        }
        request=self.factory.post('/api/v1/verify-email', request_data, format='json')
        response=self.view(request)

        self.assertEqual(response.status_code,400)

    def test_already_verified_email(self):
        self.verification_code_obj.email_verified = True
        self.verification_code_obj.save()
        request_data={
            'verification_code':self.verification_code,
            'email':self.user.email
        }
        request=self.factory.post('/api/v1/verify-email', request_data, format='json')
        response=self.view(request)

        self.assertEqual(response.status_code,400)
        print(response.data,"response")
        self.assertEqual(response.data, {"success": False, "message": "Expired verification code  or email is already verified"})


    