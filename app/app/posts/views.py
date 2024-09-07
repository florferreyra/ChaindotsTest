
from app.users.models import User
from app.posts.filters import PostFilters
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from app.common.pagination import StandardResultsSetPagination
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters import rest_framework as filters

from app.posts.models import Comment, Post

from .serializers import PostSerializer, CommentSerializer, PostRetrieveSerializer


class PostModelViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PostFilters
    queryset = Post.objects.order_by("-created_at").all()
    serializer_class = PostSerializer

    def retrieve(self, request, *args, **kwargs):
        post_id = kwargs.get('pk')
        instance = Post.objects.with_comments(pk=post_id).with_author().get(id=post_id)
        serializer = PostRetrieveSerializer(instance=instance)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    


class CommentAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        content = request.data.get('content')
        user_id = request.data.get('user_id')   
        try:
            comment = Comment.objects.create(
                post = post,
                user_id = user_id,
                content = content
            )
        except IntegrityError as _:
            msg = _.args[0]
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        serializer = CommentSerializer(instance=comment)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def get(self, request, post_id):
        comments = Comment.objects.filter(post_id=post_id)
        serializer = CommentSerializer(instance=comments, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

