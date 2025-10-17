"""
view for user
"""
from multiprocessing.pool import CLOSE

from rest_framework import generics, permissions, authentication
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
from django.shortcuts import render
from .serializers import UserSerializer,AuthTokenSerializer



class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user retrieving and updating user profile"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user

