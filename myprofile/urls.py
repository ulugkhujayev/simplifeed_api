from django.urls import path
from .views import (
    ProfileListAPIView,
    ProfileRetrieveAPIView,
    ProfileUpdateAPIView,
    ProfileDestroyAPIView,
)

urlpatterns = [
    path("profiles/", ProfileListAPIView.as_view(), name="profile-list"),
    path("profiles/<int:pk>/", ProfileRetrieveAPIView.as_view(), name="profile-detail"),
    path(
        "profiles/<int:pk>/update/",
        ProfileUpdateAPIView.as_view(),
        name="profile-update",
    ),
    path(
        "profiles/<int:pk>/delete/",
        ProfileDestroyAPIView.as_view(),
        name="profile-delete",
    ),
]
