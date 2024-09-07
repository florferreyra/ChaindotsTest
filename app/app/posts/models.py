from app.common.models import TimeStampedModel
from app.posts.managers import PostManagerQueryset
from django.db import models


class Post(TimeStampedModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(max_length=500)

    objects = PostManagerQueryset.as_manager()


class Comment(TimeStampedModel):
    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=500)
