from django.db import models
from django.contrib.auth.models import User as AuthUser
from app.users.managers import UserManager

from app.common.models import TimeStampedModel

class User(AuthUser, TimeStampedModel):
    
    objects = UserManager()


class Follow(TimeStampedModel):
    following = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="followers", blank=True, null=True)
    follower = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="following", blank=True, null=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self) -> str:
        return f"{self.follower.username} is following to {self.following.username}"