from app.posts.models import Post
from django_filters import rest_framework as filters


class PostFilters(filters.FilterSet):
    author_id = filters.NumberFilter(field_name="user_id")
    from_date = filters.DateTimeFilter(field_name="created_at", lookup_expr=('gte'))
    to_date = filters.DateTimeFilter(field_name="created_at", lookup_expr=('lte'))

    class Meta:
        model = Post 
        fields = ["author_id", "from_date", "to_date"]