from django.db import models
from django.db.models import Prefetch, Subquery


class PostManagerQueryset(models.QuerySet):
    def with_latest_comments(self, pk):
        from app.posts.models import Comment
        latest_comments = Comment.objects.filter(post_id=pk).order_by('-created_at').values_list("id", flat=True)[:3]
        return self.prefetch_related(Prefetch('comments', queryset=Comment.objects.filter(
            id__in=Subquery(latest_comments)).order_by('-created_at')))

    def with_author(self):
        return self.select_related('user')
