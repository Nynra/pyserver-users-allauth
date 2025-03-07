from django.urls import path, include
from allauth.account.views import LoginView, LogoutView

# from rest_framework import routers
# from .api import UserViewSet

# Routers provide an easy way of automatically determining the URL conf.
# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)


urlpatterns = [
    # path('api/', include('knox.urls'), name='knox'),
    # path("", include("django.contrib.auth.urls"), name="auth")
]
