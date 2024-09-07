from django.urls import path, include
from .views import CommentAPIView


urlpatterns = [
    path('posts/<int:post_id>/comments/', CommentAPIView.as_view(), name='comments'),
]