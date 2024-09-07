from django.db import models
from django.db.models import Count
from django.db.models.functions import Coalesce


class UserManager(models.Manager):
    def with_counts(self):
        return self.annotate(
            total_posts=Coalesce(Count('posts'), 0),
            total_comments=Coalesce(Count('comments'), 0)
        )
