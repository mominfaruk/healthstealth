from django.test import TestCase, Client
from django.urls import reverse
from apps.accounts.models.users import User


class UserRegisterTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Assumes that the registration url is named "user_register" in your urls.py
        self.url = reverse("user-registration")

    def test_register_user_valid(self):
        data = {
            "username": "testuser",
            "password": "Strongpassword23!",
            "password2": "Strongpassword23!",
            "email": "testuser@example.com",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
        # Verify that the user is created
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_register_user_invalid_passwords(self):
        data = {
            "username": "testuser2",
            "password": "password23!",
            "password2": "DifferentPassword",
            "email": "testuser2@example.com",
        }
        response = self.client.post(self.url, data)
        # A failed registration usually re-renders the form (status code 200)
        self.assertEqual(response.status_code, 400)
        # User should not be created
        self.assertFalse(User.objects.filter(username="testuser2").exists())

    def test_register_user_missing_username(self):
        data = {
            "username": "",
            "password": "Strongpassword23!",
            "password2": "Strongpassword23!",
            "email": "nouser@example.com",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(email="nouser@example.com").exists())