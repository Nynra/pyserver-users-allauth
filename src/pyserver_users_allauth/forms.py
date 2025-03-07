from django.contrib.auth import forms
from pyserver_users_allauth.models import User


class UserCreationForm(forms.UserCreationForm):
    """Form for creating a new user."""

    class Meta:
        model = User
        fields = ("username", "email")


class UserChangeForm(forms.UserChangeForm):
    """Form for changing a user."""

    class Meta:
        model = User
        fields = ("username", "email")
