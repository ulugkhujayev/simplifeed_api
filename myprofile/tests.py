from mixer.backend.django import mixer
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.profile = mixer.blend(UserProfile, user=self.user, age=25)

    def test_profile_destroy_unauthenticated(self):
        self.client.force_authenticate(user=None)
        url = reverse("profile-delete", kwargs={"pk": self.profile.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_update_authenticated(self):
        new_data = {
            "first_name": "New First Name",
            "last_name": "New Last Name",
            "email": "new_email@example.com",
            "age": 30,
            "gender": "male",
        }
        url = reverse("profile-update", kwargs={"pk": self.profile.pk})
        response = self.client.put(url, new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.first_name, "New First Name")
        self.assertEqual(self.profile.last_name, "New Last Name")
        self.assertEqual(self.profile.email, "new_email@example.com")
        self.assertEqual(self.profile.age, 30)

    def test_profile_update_unauthenticated(self):
        self.client.force_authenticate(user=None)
        url = reverse("profile-update", kwargs={"pk": self.profile.pk})
        response = self.client.put(url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
