import json
import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.mark.django_db
class TestAuthRegistration:

    def setup_method(self):
        self.client = Client()

    def test_register_new_user(self):
        url = reverse("api:registration")
        response = self.client.post(url, {
            "username": "newuserer",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "email": "new@user.com"
        })
        assert response.status_code == 200

    def test_register_again_user(self):
        url = reverse("api:registration")
        response = self.client.post(url, {
            "username": "newuser",
            "password1": "StrongPass123!",
            "password2": "StrongPass123",
            "email": "new@user.com"
        })
        assert response.status_code == 401
