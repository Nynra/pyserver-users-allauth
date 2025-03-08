from typing import List, Union
from django.urls import URLPattern, URLResolver, include, path
from django.views.generic.base import RedirectView
from allauth.urls import build_provider_urlpatterns
from pyserver_users_allauth.conf import settings


urlpatterns: List[Union[URLPattern, URLResolver]] = []
if not settings.HEADLESS_ONLY:
    urlpatterns += [path("", include("allauth.account.urls"))]
    if settings.MFA_ENABLED:
        urlpatterns += [path("2fa/", include("allauth.mfa.urls"))]

if settings.SOCIALACCOUNT_ENABLED and not settings.HEADLESS_ONLY:
    urlpatterns += [path("3rdparty/", include("allauth.socialaccount.urls"))]

    # DEPRECATED! -- deal with legacy URLs
    urlpatterns += [
        path(
            "social/login/cancelled/",
            RedirectView.as_view(
                pattern_name="socialaccount_login_cancelled", permanent=True
            ),
        ),
        path(
            "social/login/error/",
            RedirectView.as_view(
                pattern_name="socialaccount_login_error", permanent=True
            ),
        ),
        path(
            "social/signup/",
            RedirectView.as_view(pattern_name="socialaccount_signup", permanent=True),
        ),
        path(
            "social/connections/",
            RedirectView.as_view(
                pattern_name="socialaccount_connections", permanent=True
            ),
        ),
    ]
    # (end DEPRECATED)

if settings.SOCIALACCOUNT_ENABLED:
    urlpatterns += build_provider_urlpatterns()

if settings.USERSESSIONS_ENABLED and not settings.HEADLESS_ONLY:
    urlpatterns += [path("sessions/", include("allauth.usersessions.urls"))]
