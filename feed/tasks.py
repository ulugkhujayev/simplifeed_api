from django.utils import timezone
from datetime import timedelta
from .utils import generate_pdf
from .serializers import PostSerializer
from .models import Post
from celery import shared_task


@shared_task
def generate_recent_posts_pdf():
    start_date = timezone.now() - timedelta(hours=24)
    end_date = timezone.now()
    queryset = Post.objects.filter(created_at__range=(start_date, end_date))

    serializer = PostSerializer(queryset, many=True)
    serialized_data = serializer.data

    posts = [
        {
            "id": data["id"],
            "author": str(data["author"]),
            "body": data["body"],
            "created_at": data["created_at"],
            "updated_at": data["updated_at"],
        }
        for data in serialized_data
    ]

    return generate_pdf(posts)
