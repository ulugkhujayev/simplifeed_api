from rest_framework import serializers
from .models import Post, Comment, Like, Repost
from myprofile.serializers import CustomUserSerializer


class PostSerializer(serializers.ModelSerializer):
    # author = CustomUserSerializer()

    class Meta:
        model = Post
        fields = ["id", "author", "body", "draft", "created_at", "updated_at"]
        read_only_fields = ["author"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "author",
            "comment_text",
            "post",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["author"]
