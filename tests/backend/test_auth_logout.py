import json
import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

uname = "testuser"
pswd = "password123"
usrmail = "random@mail.com"

@pytest.mark.django_db
class TestAuthLogout:

    # Create test user
    def setup_method(self):
        self.user = User.objects.create_user(
            username=uname,
            password=pswd,
            email=usrmail,
        )
        self.client = Client()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.refresh_token = str(refresh)

    def test_logout_valid_token(self):
        url = reverse("api:logout")  # adjust namespace if needed
        response = self.client.post(
            url,
            data=json.dumps({"refresh": self.refresh_token}),
            content_type="application/json"
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["status"] == "success"

    def test_logout_invalid_token(self):
        url = reverse("api:logout")
        response = self.client.post(
            url,
            data=json.dumps({"refresh": "invalidtoken123"}),
            content_type="application/json"
        )
        # Your view currently returns 200 with error message for invalid token
        assert response.status_code == 401
        data = json.loads(response.content)
        assert data["status"] == "error"
