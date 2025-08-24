import json
import pytest

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

uname = "testuser"
nxuser = "nonexistentusr"
pswd = "passwordtotest1234"
wrongpswd = "wrongpassword1234"
usrmail = "random@mail.com"

@pytest.mark.django_db 
class TestAuthLogin:

    def setup_method(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username=uname, 
            password=pswd, 
            email=usrmail,
        )

    def test_login_valid_creds(self):

        client = Client()
        url = reverse('api:login')
        response = client.post(url, {
            "username": uname,
            "password": pswd,
        })

        assert response.status_code == 200
        
        data = json.loads(response.content)
        assert data['status'] == 'success'
        assert 'access' in data

    def test_login_invalid_creds(self):

        client = Client()
        url = reverse('api:login')
        response = client.post(url, {
            "username": uname,
            "password": wrongpswd,
        })

        assert response.status_code == 401
        
        data = json.loads(response.content)
        assert data['status'] == 'error'
        assert 'access' not in data

    def test_login_nxuser(self):

        client = Client()
        url = reverse('api:login')
        response = client.post(url, {
            "username": nxuser,
            "password": pswd,
        })

        assert response.status_code == 401
        
        data = json.loads(response.content)
        assert data['status'] == 'error'
        assert 'access' not in data