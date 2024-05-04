from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication

from .serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
