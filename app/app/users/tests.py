import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
class TestUser:
    def setup(self):
        self.client = APIClient()
        self.user = User.objects.create(username="testuser", password="testpass")
        

    def test_user_model_viewset_with_authenticated_user(self):
        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token.access_token)}')
        url = reverse('users-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_user_model_viewset_with_unauthenticated_user(self):
        url = reverse('users-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


