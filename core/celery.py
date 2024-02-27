# celery.py
import os
from celery import Celery, signals

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.broker_url = "redis://localhost:6379/0"

app.autodiscover_tasks()

app.conf.update(
    CELERY_FLOWER_USER="username",
    CELERY_FLOWER_PASSWORD="password",
    CELERY_FLOWER_PORT=5555,
)


# @signals.worker_ready.connect
# def on_worker_ready(**kwargs):
#     from flower.command import Flower

#     flower_app = Flower()
#     flower_app.execute_from_commandline(argv=["flower"])
