from rest_framework.permissions import BasePermission
from .models import UserProfile


class IsProfileOwner(BasePermission):
    def has_permission(self, request, view):
        try:
            profile = UserProfile.objects.get(pk=view.kwargs["pk"])
        except UserProfile.DoesNotExist:
            return False
        return profile.user == request.user
