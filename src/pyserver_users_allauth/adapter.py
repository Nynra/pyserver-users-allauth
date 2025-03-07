from allauth.account.adapter import DefaultAccountAdapter
from .models import User


class SocialAccountAdapter(DefaultAccountAdapter):
    """Accountadapter for Social Account.

    This class is used to create new users from social logins
    """

    # def is_open_for_signup(self, request, socialaccount):

    #     return False

    def save_user(self, request, form=None):
        """Save the user model to the database.

        The `form` parameter will be `None` if `AUTO_SIGNUP` is used
        """
        data = form.cleaned_data
        user = User()

        # Set the username and email
        user.username = data.get("username")
        user.email = data.get("email")

        # Check if there is a password
        if "password1" in data:
            user.set_password(data["password1"])
        elif "password" in data:
            user.set_password(data["password"])
        else:
            user.set_unusable_password()

        # Save the user
        user.save()
        return user
