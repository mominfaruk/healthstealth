from django.test import TestCase, override_settings
from rest_framework.test import APIRequestFactory
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import jwt

from django.conf import settings
from apps.accounts.models.users import User
from apps.accounts.models.verification_code import VerificationCode
from apps.accounts.views.user_registration import UserRegistration
from healthstealth.configs.email_template_settings import EMAIL_TEMPLATES

@override_settings(
    SECRET_KEY='test_secret_key',
    DEFAULT_FROM_EMAIL='test@example.com',
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'
)
class UserRegistrationTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = UserRegistration.as_view()
        self.valid_payload = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'StrongPass123!',
            'password2': 'StrongPass123!'  # Add confirmation password
        }
        self.invalid_payload = {
            'username': '',
            'email': 'invalid-email',
            'password': 'short',
            'password2': 'different'
        }

    @patch('apps.gist.views.email.EmailService.send_email')
    @patch('apps.gist.views.logger.LogHelper.fail_log')
    def test_successful_user_registration(self, mock_fail_log, mock_send_email):
        request = self.factory.post('/register/', self.valid_payload, format='json')
        response = self.view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {"success": True, "message": "User created successfully"})

        # Verify user creation
        user = User.objects.get(email=self.valid_payload['email'])
        self.assertIsNotNone(user)

        # Verify verification code creation
        verification_code_obj = VerificationCode.objects.get(user=user)
        self.assertIsNotNone(verification_code_obj)

        # Verify email was sent
        mock_send_email.assert_called_once()
        mock_fail_log.assert_not_called()

    @patch('apps.gist.views.email.EmailService.send_email')
    @patch('apps.gist.views.logger.LogHelper.fail_log')
    def test_invalid_data_registration(self, mock_fail_log, mock_send_email):
        request = self.factory.post('/register/', self.invalid_payload, format='json')
        response = self.view(request)

        self.assertEqual(response.status_code, 400)
        
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(email=self.invalid_payload['email'])

        mock_send_email.assert_not_called()
        mock_fail_log.assert_not_called()


    def test_jwt_token_generation(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='StrongPass123!'
        )
        verification_code = '123456'

        token = jwt.encode({
            'user_id': user.id,
            'verification_code': verification_code,
            'exp': datetime.now() + timedelta(minutes=15)
        }, settings.SECRET_KEY, algorithm='HS256')

        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        self.assertEqual(decoded_token['user_id'], user.id)
        self.assertEqual(decoded_token['verification_code'], verification_code)

    @patch('apps.gist.views.email.EmailService.send_email')
    def test_email_sending(self, mock_send_email):
        request = self.factory.post('/register/', self.valid_payload, format='json')
        response = self.view(request)

        self.assertEqual(response.status_code, 201)
        
        user = User.objects.get(email=self.valid_payload['email'])
        verification_code = VerificationCode.objects.get(user=user)

        # Get the actual call arguments
        call_args = mock_send_email.call_args[1]
        
        # Define the expected subject with the correct quotation marks
        expected_subject = "Please Verify Your Email Address"
        
        # Verify each argument separately
        self.assertEqual(call_args['recipients'], [self.valid_payload['email']])
        self.assertEqual(call_args['subject'], expected_subject)
        self.assertEqual(call_args['template_name'], EMAIL_TEMPLATES.get('user_registration_verification'))
        self.assertEqual(call_args['from_email'], settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(call_args['email_type'], 'verification')
        
        # Verify context contains required keys
        self.assertIn('verification_token', call_args['context'])
        self.assertIn('verification_code', call_args['context'])
        self.assertEqual(call_args['context']['verification_code'], verification_code.email_verification_code)

    @patch('apps.gist.views.email.EmailService.send_email')
    @patch('apps.gist.views.logger.LogHelper.fail_log')
    def test_invalid_data_registration(self, mock_fail_log, mock_send_email):
        request = self.factory.post('/register/', self.invalid_payload, format='json')
        try:
            response = self.view(request)
            
            # Ensure response indicates validation error
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', response.data)
            
            # Verify no user was created
            with self.assertRaises(User.DoesNotExist):
                User.objects.get(email=self.invalid_payload['email'])

            # Verify no email was sent
            mock_send_email.assert_not_called()
            mock_fail_log.assert_not_called()
            
        except Exception as e:
            self.fail(f"Test failed with exception: {str(e)}")

   