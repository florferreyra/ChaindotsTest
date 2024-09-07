from app.posts.models import Comment, Post
from app.users.serializers import UserFollowSerializer
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class PostRetrieveSerializer(serializers.ModelSerializer):
    user = UserFollowSerializer()
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'
