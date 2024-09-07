from django.urls import path

from .views import FollowAPIView

urlpatterns = [
    path('users/<int:user_id>/follow/<int:follow_id>/', FollowAPIView.as_view(), name='follow'),
]
