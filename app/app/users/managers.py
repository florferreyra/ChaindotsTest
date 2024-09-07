from django.db import models
from django.db.models import Count
from django.db.models.functions import Coalesce


class UserManager(models.Manager):
    def with_counts(self):
        """
        Annotate users with counts of related posts and comments.

        This method extends the queryset to include annotations for the total number of posts
        and comments associated with each user. If a user has no related posts or comments, 
        the count is set to 0.

        Returns:
            QuerySet: A queryset of users with additional annotations for `total_posts` and `total_comments`.
        """
        return self.annotate(
            total_posts=Coalesce(Count('posts'), 0),
            total_comments=Coalesce(Count('comments'), 0)
        )
