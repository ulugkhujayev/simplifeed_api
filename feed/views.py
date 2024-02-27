import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import generics
from django.utils import timezone
from datetime import timedelta
from django.db.models import Prefetch
from .utils import generate_pdf
from .serializers import (
    PostSerializer,
    CommentSerializer,
)
from .models import Post, Comment, Like, Repost, PostView

logger = logging.getLogger(__name__)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.prefetch_related(
        Prefetch("comment_set", queryset=Comment.objects.select_related("author")),
        "like_set",
        "repost_set",
    ).all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def list(self, request, *args, **kwargs):
        user = self.request.user
        viewed_posts = PostView.objects.filter(user=user).values_list(
            "post_id", flat=True
        )
        queryset = self.get_queryset().exclude(id__in=viewed_posts)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        PostView.objects.get_or_create(user=request.user, post=instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("author").all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post_id = self.request.data.get("post_id")
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise NotFound("Post matching query does not exist.")
        serializer.save(author=self.request.user, post=post)


class LikeViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        post_id = self.kwargs.get("post_pk")
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND
            )

        like, created = Like.objects.get_or_create(author=request.user, post=post)
        if not created:
            like.delete()
            return Response(
                {"detail": "Post like removed."}, status=status.HTTP_204_NO_CONTENT
            )

        return Response(
            {"detail": "Post liked successfully."},
            status=status.HTTP_201_CREATED,
        )

    def list(self, request, *args, **kwargs):
        post_id = self.kwargs.get("post_pk")
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND
            )

        num_likes = post.like_set.count()
        return Response({"num_likes": num_likes}, status=status.HTTP_200_OK)


class RepostViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        post_id = self.kwargs.get("post_pk")
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND
            )

        repost, created = Repost.objects.get_or_create(author=request.user, post=post)
        if not created:
            repost.delete()
            return Response(
                {"detail": "Repost removed."},
                status=status.HTTP_204_NO_CONTENT,
            )

        return Response(
            {"detail": "Post reposted successfully."},
            status=status.HTTP_201_CREATED,
        )

    def list(self, request, *args, **kwargs):
        post_id = self.kwargs.get("post_pk")
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND
            )

        num_reposts = post.repost_set.count()
        return Response({"num_reposts": num_reposts}, status=status.HTTP_200_OK)


class RecentPostsPDFView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    start_date = timezone.now() - timedelta(hours=24)
    end_date = timezone.now()
    queryset = Post.objects.filter(created_at__range=(start_date, end_date))

    def get(self, request, *args, **kwargs):
        posts = self.get_queryset()
        pdf_content = generate_pdf(posts)
        return Response(pdf_content, content_type="application/pdf")


@api_view(["GET"])
def overall_post_views(request, post_id):
    post = Post.objects.get(id=post_id)
    post_views_count = PostView.objects.filter(post=post).count()
    return Response({"post_id": post_id, "overall_views": post_views_count})
