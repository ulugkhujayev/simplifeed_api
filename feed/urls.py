from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PostViewSet,
    CommentViewSet,
    LikeViewSet,
    RepostViewSet,
    RecentPostsPDFView,
    overall_post_views,
)

router = DefaultRouter()
router.register(r"posts", PostViewSet)
router.register(r"comments", CommentViewSet)

urlpatterns = [
    path(
        "feed/posts/<int:post_pk>/like/",
        LikeViewSet.as_view({"post": "create", "get": "list"}),
        name="like-post",
    ),
    path(
        "feed/posts/<int:post_pk>/repost/",
        RepostViewSet.as_view({"post": "create", "get": "list"}),
        name="repost-post",
    ),
    path("posts/<int:post_id>/views/", overall_post_views, name="overall-post-views"),
    path("generate_pdf/", RecentPostsPDFView.as_view(), name="generate_pdf"),
]

urlpatterns += router.urls
