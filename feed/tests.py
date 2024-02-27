from unittest.mock import patch
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from myprofile.models import CustomUser as User
from .models import Post, PostView
from rest_framework.response import Response


class PostAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(author=self.user, body="Test post")

    @patch("feed.views.PostViewSet.get_queryset")
    def test_post_list_api(self, mock_get_queryset):
        mock_get_queryset.return_value = Post.objects.none()
        url = reverse("post-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_retrieve_api(self):
        url = reverse("post-detail", kwargs={"pk": self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("feed.views.PostViewSet.get_object")
    def test_post_retrieve_api_viewed(self, mock_get_object):
        mock_get_object.return_value = self.post
        url = reverse("post-detail", kwargs={"pk": self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            PostView.objects.filter(user=self.user, post=self.post).exists()
        )

    @patch("feed.views.CommentViewSet.perform_create")
    def test_comment_create_api(self, mock_perform_create):
        mock_perform_create.return_value = None
        url = reverse("comment-list")
        data = {
            "author": self.user.pk,
            "comment_text": "Test comment",
            "post": self.post.pk,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch("feed.views.LikeViewSet.create")
    def test_like_create_api(self, mock_like_create):
        mock_response = Response(
            {"detail": "Post liked successfully."}, status=status.HTTP_201_CREATED
        )
        mock_like_create.return_value = mock_response
        url = reverse("like-post", kwargs={"post_pk": self.post.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch("feed.views.RepostViewSet.create")
    def test_repost_create_api(self, mock_repost_create):
        mock_response = Response(
            {"detail": "Post reposted successfully."}, status=status.HTTP_201_CREATED
        )
        mock_repost_create.return_value = mock_response
        url = reverse("repost-post", kwargs={"post_pk": self.post.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch("feed.views.RecentPostsPDFView.get_queryset")
    @patch("feed.views.generate_pdf")
    def test_recent_posts_pdf_api(self, mock_generate_pdf, mock_get_queryset):
        mock_generate_pdf.return_value = b"PDF body"
        url = reverse("generate_pdf")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content.strip(b'"'), b"PDF body")

    @patch("feed.views.Post.objects.get")
    @patch("feed.views.PostView.objects.filter")
    def test_overall_post_views_api(self, mock_post_view_filter, mock_post_get):
        mock_post_get.return_value = self.post
        mock_post_view_filter.return_value.count.return_value = 5
        url = reverse("overall-post-views", kwargs={"post_id": self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["overall_views"], 5)
