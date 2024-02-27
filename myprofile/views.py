from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer
from .models import UserProfile
from .permissions import IsProfileOwner


class ProfileListAPIView(ListAPIView):
    queryset = UserProfile.objects.select_related("user").all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)


class ProfileRetrieveAPIView(RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = UserProfile.objects.select_related("user").all()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(is_public=True) | queryset.filter(
                user=self.request.user
            )
        else:
            queryset = queryset.filter(is_public=True)
        return queryset


class ProfileUpdateAPIView(UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]

    def get_queryset(self):
        return UserProfile.objects.select_related("user").filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class ProfileDestroyAPIView(DestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]

    def get_queryset(self):
        return UserProfile.objects.select_related("user").filter(user=self.request.user)
