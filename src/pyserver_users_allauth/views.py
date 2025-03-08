from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class ProfileSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'users_allauth/profile_settings.html'