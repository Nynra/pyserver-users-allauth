from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils import timezone
from django.db import models
from pyserver_users_allauth.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """This class represents the user authentication model."""

    # Account info
    username = models.CharField(max_length=30, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)

    # Django permission fields
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def __str__(self):
        """Return the string representation of the user."""
        return self.username

    def save(self, *args, **kwargs):
        """Save the user model to the database."""
        self.full_clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Get the absolute URL of the user."""
        return f"/users/{self.pk}/"
