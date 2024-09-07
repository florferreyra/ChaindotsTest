from django.db import models
from django.db.models import Prefetch, Subquery


class PostManagerQueryset(models.QuerySet):
    def with_latest_comments(self, pk):
        """
        Annotates the queryset with the latest comments for a given post.

        This method filters comments related to the post with the provided primary key (`pk`), 
        orders them by creation date in descending order, and selects the three most recent comments.
        It then prefetches these latest comments for the posts in the queryset.

        Args:
            pk (int): The primary key of the post for which to fetch the latest comments.

        Returns:
            QuerySet: The queryset with the latest comments pre-fetched.
        """
        from app.posts.models import Comment
        latest_comments = Comment.objects.filter(post_id=pk).order_by('-created_at').values_list("id", flat=True)[:3]
        return self.prefetch_related(Prefetch('comments', queryset=Comment.objects.filter(
            id__in=Subquery(latest_comments)).order_by('-created_at')))

    def with_author(self):
        """
        Annotates the queryset with the related author (user) of each post.

        This method performs a SQL join to include the related `user` object for each post in the queryset, 
        allowing access to the author's details.

        Returns:
            QuerySet: The queryset with the related author (user) included.
        """
        return self.select_related('user')
