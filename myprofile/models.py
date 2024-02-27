from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser, Group, Permission


class CustomUser(AbstractUser):
    age = models.IntegerField(
        _("Age"),
        validators=[
            MinValueValidator(13, _("Minimum age requirement not met.")),
            MaxValueValidator(120, _("Invalid age")),
        ],
        null=True,
        blank=True,
    )
    gender = models.CharField(
        _("Gender"),
        max_length=20,
        choices=[
            ("male", "Male"),
            ("female", "Female"),
            ("undisclosed", _("Undisclosed")),
        ],
        null=True,
        blank=True,
    )

    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        related_name="custom_users",
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        related_name="custom_users",
        related_query_name="custom_user",
        help_text=_("Specific permissions for this user."),
    )


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.PROTECT)
    avatar = models.ImageField(
        upload_to="avatars/%Y/%m/%d/",
        blank=True,
        null=True,
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    age = models.IntegerField(default=18)
    gender = models.CharField(
        max_length=12,
        choices=[
            ("male", "Male"),
            ("female", "Female"),
            ("undisclosed", _("Undisclosed")),
        ],
    )
    is_public = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user.username}'s profile"
