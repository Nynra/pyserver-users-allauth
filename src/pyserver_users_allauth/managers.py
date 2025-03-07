from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy


class UserManager(BaseUserManager):
    """
    Custom user model manager where username is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, username: str, email: str, password, **extra_fields):
        """
        Create and save a user with the given username and password.

        Parameters
        ----------
        username : str
            The username of the user
        email : str
            The email of the user
        password : str
            The password of the user

        Returns
        -------
        user
            The created user model.
        """
        if not username:
            raise ValueError(gettext_lazy("The Username must be set"))
        if not password:
            raise ValueError(gettext_lazy("The Password must be set"))
        if not email:
            raise ValueError(gettext_lazy("The Email must be set"))

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self, username: str, email: str, password: str, **extra_fields
    ):
        """
        Create and save a SuperUser with the given username and password.

        Parameters
        ----------
        username : str
            The username of the user
        email : str
            The email of the user
        password : str
            The password of the user

        Returns
        -------
        user
            The created user model for the superuser.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") != True:
            raise ValueError(gettext_lazy("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") != True:
            raise ValueError(gettext_lazy("Superuser must have is_superuser=True."))
        if extra_fields.get("is_active") != True:
            raise ValueError(gettext_lazy("Superuser must have is_active=True."))

        return self.create_user(
            username=username, password=password, email=email, **extra_fields
        )
