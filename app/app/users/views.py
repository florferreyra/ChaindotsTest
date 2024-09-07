from app.users.models import Follow, User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import UserCreateSerializer, UserSerializer


class UserModelViewSet(ModelViewSet):
    """
    A viewset for managing user instances.

    This viewset provides the CRUD actions for user instances.
    It uses JWT authentication and requires the user to be authenticated to access the endpoints.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.with_counts().all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserCreateSerializer
        return UserSerializer


class FollowAPIView(APIView):
    """
    An API view for managing user follow actions.

    This view allows authenticated users to follow other users. 
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id, follow_id):
        """
        Create a follow relationship between two users.

        Args:
            user_id (int): The ID of the user initiating the follow action.
            follow_id (int): The ID of the user to be followed.

        Returns:
            Response: 
                - 200 OK if the follow relationship is created successfully.
                - 400 Bad Request if the follow relationship already exists.
        """
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
