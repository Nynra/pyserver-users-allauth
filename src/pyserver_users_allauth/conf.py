from django.conf import settings
from appconf import AppConf


class PyserverUsersAllauthConf(AppConf):
    ADMIN_GROUP_NAME = "admins"
    USERNAME_BLACKLIST = [
        "admin",
        "superuser",
        "root",
        "user",
        "users",
        "username",
    ]

    # Enable or disble views (usefull for when a custom view is used)
    ENABLE_DEFAULT_LOGIN_VIEW = True
    ENABLE_DEFAULT_LOGOUT_VIEW = True
    ENABLE_DEFAULT_SIGNUP_VIEW = True
    ENABLE_DEFAULT_PROFILE_VIEW = True

    # Some allauth settings
    HEADLESS_ONLY = False
    MFA_ENABLED = False
    SOCIALACCOUNT_ENABLED = False
    USERSESSIONS_ENABLED = False

    class Meta:
        # Make this setting module a proxy for the global settings
        # so we can use this module to access all the settings
        proxy = True
        prefix = "users_allauth"
