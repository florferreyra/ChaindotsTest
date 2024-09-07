from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from app.users.models import Follow, User

from .serializers import UserCreateSerializer, UserSerializer


class UserModelViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.with_counts().all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserCreateSerializer
        return UserSerializer


class FollowAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id, follow_id):
        user = get_object_or_404(User, id=user_id)
        follow_user = get_object_or_404(User, id=follow_id)
        try:
            follow = Follow.objects.create(
                follower=user,
                following=follow_user
            )
        except IntegrityError as _:
            msg = f"{user.username} is already following to {follow_user.username}"
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_200_OK, data=follow.__str__())
