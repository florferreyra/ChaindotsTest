import pytest
from app.posts.models import Comment, Post
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
class TestUser:
    """
    Test suite for the User API endpoints.

    This class contains tests for the User viewset, including authentication scenarios.
    """
    def setup_method(self):
        """
        Set up the test environment.

        Creates a test user and initializes the API client.
        """
        self.client = APIClient()
        self.user = User.objects.create(username="testuser", password="testpass")

    def test_user_model_viewset_with_authenticated_user(self):
        """
        Test accessing the user list endpoint with an authenticated user.

        Creates an access token for the test user, adds it to the request headers, and verifies that
        the user list endpoint returns a 200 OK status.
        """
        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token.access_token)}')
        url = reverse('users-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_user_model_viewset_with_unauthenticated_user(self):
        """
        Test accessing the user list endpoint with an unauthenticated user.

        Sends a request to the user list endpoint without authentication and verifies that the response
        status code is 401 Unauthorized.
        """
        url = reverse('users-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
