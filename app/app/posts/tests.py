from datetime import datetime, timedelta

import pytest
from app.posts.models import Comment, Post
from app.users.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestPosts:
    """
    Test suite for the Post API endpoints.

    This class contains tests for listing posts with filters and retrieving a post with its comments.
    """
    def setup_method(self):
        """
        Set up the test environment.

        Creates a test user and authenticates the API client.
        """
        self.client = APIClient()
        self.user = User.objects.create(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)

    def test_post_list_with_user_filter(self):
        """
        Test listing posts with a filter for the author.

        Creates two posts for the authenticated user and verifies that the list endpoint returns both posts
        when filtered by the author's ID.
        """
        Post.objects.create(user=self.user, content="Post 1", created_at=timezone.now())
        Post.objects.create(user=self.user, content="Post 2", created_at=timezone.now())

        url = reverse('posts-list')
        response = self.client.get(url, {'author_id': self.user.id})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2

    def test_post_list_with_date_filters(self):
        """
        Test listing posts with date filters.

        Creates two posts with different creation dates and verifies that the list endpoint returns both posts
        when filtering by date range.
        """
        self.client.force_authenticate(user=self.user)

        now_str = "2024-09-07 18:00"
        now = datetime.strptime(now_str, "%Y-%m-%d %H:%M")
        created_at_1 = now - timedelta(days=2)
        created_at_2 = now - timedelta(days=1)

        Post.objects.create(user=self.user, content="Post 1", created_at=created_at_1)
        Post.objects.create(user=self.user, content="Post 2", created_at=created_at_2)

        url = reverse('posts-list')
        from_date = (now - timedelta(days=3)).strftime("%Y-%m-%d %H:%M")
        response = self.client.get(url, {'author_id': self.user.id,
                                         'from_date': from_date,
                                         'to_date': '2024-09-08 18:00'
                                         }
                                   )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2

    @pytest.mark.django_db
    def test_post_retrieve_with_comments(self):
        """
        Test retrieving a post with its latest comments.

        Creates a post with multiple comments and verifies that the retrieve endpoint returns the post
        along with the three most recent comments.
        """
        post = Post.objects.create(user=self.user, content="Post with comments")

        Comment.objects.create(post=post, user=self.user, content="Comment 1")
        Comment.objects.create(post=post, user=self.user, content="Comment 2")
        Comment.objects.create(post=post, user=self.user, content="Comment 3")
        Comment.objects.create(post=post, user=self.user, content="Comment 4")

        url = reverse('posts-detail', kwargs={'pk': post.id})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['comments']) == 3
        assert response.data['comments'][0]['content'] == "Comment 4"


@pytest.mark.django_db
class TestComments:
    """
    Test suite for the Comment API endpoints.

    This class contains tests for creating a comment and listing comments for a specific post.
    """
    def setup_method(self):
        """
        Set up the test environment.

        Creates a test user and authenticates the API client.
        """
        self.client = APIClient()
        self.user = User.objects.create(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)

    def test_comment_create(self):
        """
        Test creating a new comment for a post.

        Creates a post and then creates a comment associated with that post. Verifies that the comment
        creation endpoint returns the correct data.
        """
        post = Post.objects.create(user=self.user, content="A post to comment")

        data = {
            "content": "A new comment",
            "user_id": self.user.id
        }

        url = reverse('comments', kwargs={'post_id': post.id})
        response = self.client.post(url, data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['content'] == "A new comment"
        assert int(response.data['user']) == self.user.id

    def test_comment_list(self):
        """
        Test listing comments for a post.

        Creates a post with multiple comments and verifies that the list endpoint returns all comments
        associated with the post.
        """
        post = Post.objects.create(user=self.user, content="A post with comments")

        Comment.objects.create(post=post, user=self.user, content="Comment 1")
        Comment.objects.create(post=post, user=self.user, content="Comment 2")

        url = reverse('comments', kwargs={'post_id': post.id})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]['content'] == "Comment 1"
