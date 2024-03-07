from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from materials.permissions import IsOwner, IsModerator
from users.models import User

from users.serializers.users import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserDetailAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]