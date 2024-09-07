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
    def setup(self):
        self.client = APIClient()
        self.user = User.objects.create(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)

    def test_post_list_with_user_filter(self):
        Post.objects.create(user=self.user, content="Post 1", created_at=timezone.now())
        Post.objects.create(user=self.user, content="Post 2", created_at=timezone.now())

        url = reverse('posts-list')
        response = self.client.get(url, {'author_id': self.user.id})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2

    def test_post_list_with_date_filters(self):
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
    def setup(self):
        self.client = APIClient()
        self.user = User.objects.create(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)

    def test_comment_create(self):
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
        post = Post.objects.create(user=self.user, content="A post with comments")

        Comment.objects.create(post=post, user=self.user, content="Comment 1")
        Comment.objects.create(post=post, user=self.user, content="Comment 2")

        url = reverse('comments', kwargs={'post_id': post.id})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]['content'] == "Comment 1"
