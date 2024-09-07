from app.users.models import User
from rest_framework import serializers


class UserFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class UserSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField(source="get_followers")
    following = serializers.SerializerMethodField(source="get_following")
    total_posts = serializers.IntegerField()
    total_comments = serializers.IntegerField()

    class Meta:
        model = User
        fields = "__all__"

    def get_followers(self, obj):
        followers = obj.followers.all()
        return [UserFollowSerializer(follower.follower).data for follower in followers]

    def get_following(self, obj):
        following = obj.following.all()
        return [UserFollowSerializer(follow.following).data for follow in following]


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email"]
