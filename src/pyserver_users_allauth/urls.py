from django.urls import path, include
from pyserver_users_allauth.views import ProfileSettingsView

urlpatterns = [
    path('profile/', ProfileSettingsView.as_view(), name='profile_settings'),
    path('', include('allauth.urls')),
]