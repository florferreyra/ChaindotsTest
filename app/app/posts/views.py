from app.common.pagination import StandardResultsSetPagination
from app.posts.filters import PostFilters
from app.posts.models import Comment, Post
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import (CommentSerializer, PostRetrieveSerializer,
                          PostSerializer)


class PostModelViewSet(ModelViewSet):
    """
    A viewset for managing `Post` instances.

    This viewset provides CRUD operations for posts, with JWT authentication, 
    pagination, and filtering capabilities.

    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PostFilters
    queryset = Post.objects.order_by("-created_at").all()
    serializer_class = PostSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific `Post` instance along with its latest comments and author details.

        This method overrides the default `retrieve` action to include the latest comments and 
        author information for the requested post.

        """
        post_id = kwargs.get('pk')
        instance = Post.objects.with_latest_comments(pk=post_id).with_author().get(id=post_id)
        serializer = PostRetrieveSerializer(instance=instance)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class CommentAPIView(APIView):
    """
    A view for managing comments on a specific post.

    This view provides methods to create a new comment and retrieve all comments for a given post, 
    with JWT authentication and permission requirements.

    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        """
        Create a new comment for a specified post.

        This method handles the creation of a new comment associated with the given post ID. 
        It extracts the comment content and user ID from the request data, creates the comment, 
        and returns a response with the serialized comment data.

        """
        post = get_object_or_404(Post, id=post_id)
        content = request.data.get('content')
        user_id = request.data.get('user_id')
        try:
            comment = Comment.objects.create(
                post=post,
                user_id=user_id,
                content=content
            )
        except IntegrityError as _:
            msg = _.args[0]
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        serializer = CommentSerializer(instance=comment)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def get(self, request, post_id):
        """
        Retrieve all comments for a specified post.

        This method retrieves all comments associated with the given post ID and returns them 
        in a serialized format.

        """
        comments = Comment.objects.filter(post_id=post_id)
        serializer = CommentSerializer(instance=comments, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
