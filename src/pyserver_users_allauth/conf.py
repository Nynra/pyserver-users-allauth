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

    class Meta:
        # Make this setting module a proxy for the global settings
        # so we can use this module to access all the settings
        proxy = True
