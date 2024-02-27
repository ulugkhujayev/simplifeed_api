from django.contrib import admin
from .models import Post, Comment, Like, Repost, PostView


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "body", "created_at", "updated_at", "draft")
    list_filter = ("author", "created_at", "updated_at", "draft")
    search_fields = ("author", "body")
    date_hierarchy = "created_at"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "created_at", "updated_at")
    list_filter = ("post__author", "created_at", "updated_at")
    search_fields = ("post__author",)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "post",
    )
    list_filter = ("post__author",)


@admin.register(Repost)
class RepostAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "created_at", "updated_at")
    list_filter = ("post__author", "created_at", "updated_at")


@admin.register(PostView)
class PostViewAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "viewed_at")
