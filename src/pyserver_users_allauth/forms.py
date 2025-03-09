from django.contrib.auth import forms as auth_forms
from django.contrib.auth import password_validation
from pyserver_users_allauth.models import User
from django import forms
from allauth.account.forms import (
    SignupForm,
    LoginForm,
)
from allauth.account import app_settings
from allauth.account.app_settings import AuthenticationMethod
from allauth.utils import get_username_max_length, set_form_field_order
from django.utils.translation import gettext_lazy as _, pgettext
from django.urls import reverse, NoReverseMatch
from django.utils.safestring import mark_safe


class AdminUserCreationForm(auth_forms.UserCreationForm):
    """Form for creating a user in the admin interface."""

    class Meta:
        model = User
        fields = ("username", "email")


class AdminUserChangeForm(auth_forms.UserChangeForm):
    """Form for changing a user in the admin interface."""

    class Meta:
        model = User
        fields = ("username", "email")


class PasswordField(forms.CharField):
    def __init__(self, *args, **kwargs):
        render_value = kwargs.pop(
            "render_value", app_settings.PASSWORD_INPUT_RENDER_VALUE
        )
        kwargs["widget"] = forms.PasswordInput(
            render_value=render_value,
            attrs={"placeholder": kwargs.get("label"), "class": "form-control"},
        )
        autocomplete = kwargs.pop("autocomplete", None)
        if autocomplete is not None:
            kwargs["widget"].attrs["autocomplete"] = autocomplete
        super(PasswordField, self).__init__(*args, **kwargs)


class PyserverSignupForm(SignupForm):
    """Form for signing up a user."""
    username = forms.CharField(
        label=_("Username"),
        max_length=get_username_max_length(),
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Username"),
                "autocomplete": "username",
                "class": "form-control",
            }
        ),
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                "placeholder": _("Email address"),
                "autocomplete": "email",
                "class": "form-control",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        self.by_passkey = kwargs.pop("by_passkey", False)
        super(SignupForm, self).__init__(*args, **kwargs)
        if not self.by_passkey:
            self.fields["password1"] = PasswordField(
                label=_("Password"),
                autocomplete="new-password",
                help_text=password_validation.password_validators_help_text_html(),
            )
            if app_settings.SIGNUP_PASSWORD_ENTER_TWICE:
                self.fields["password2"] = PasswordField(
                    label=_("Password (again)"), autocomplete="new-password"
                )

        if hasattr(self, "field_order"):
            set_form_field_order(self, self.field_order)

        honeypot_field_name = app_settings.SIGNUP_FORM_HONEYPOT_FIELD
        if honeypot_field_name:
            self.fields[honeypot_field_name] = forms.CharField(
                required=False,
                label="",
                widget=forms.TextInput(
                    attrs={
                        "style": "position: absolute; right: -99999px;",
                        "tabindex": "-1",
                        "autocomplete": "nope",
                        "class": "form-control",
                    }
                ),
            )


class PyserverLoginForm(LoginForm):
    """Form for logging in a user."""

    password = PasswordField(label=_("Password"), autocomplete="current-password")
    remember = forms.BooleanField(
        label=_("Remember Me"),
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    user = None

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(LoginForm, self).__init__(*args, **kwargs)
        if app_settings.AUTHENTICATION_METHOD == AuthenticationMethod.EMAIL:
            login_widget = forms.EmailInput(
                attrs={
                    "placeholder": _("Email address"),
                    "autocomplete": "email",
                    "class": "form-control",
                }
            )
            login_field = forms.EmailField(label=_("Email"), widget=login_widget)
        elif app_settings.AUTHENTICATION_METHOD == AuthenticationMethod.USERNAME:
            login_widget = forms.TextInput(
                attrs={
                    "placeholder": _("Username"),
                    "autocomplete": "username",
                    "class": "form-control",
                }
            )
            login_field = forms.CharField(
                label=_("Username"),
                widget=login_widget,
                max_length=get_username_max_length(),
            )
        else:
            assert (
                app_settings.AUTHENTICATION_METHOD
                == AuthenticationMethod.USERNAME_EMAIL
            )  # nosec
            login_widget = forms.TextInput(
                attrs={
                    "placeholder": _("Username or email"),
                    "autocomplete": "email",
                    "class": "form-control",
                }
            )
            login_field = forms.CharField(
                label=pgettext("field label", "Login"), widget=login_widget
            )
        self.fields["login"] = login_field
        set_form_field_order(self, ["login", "password", "remember"])
        if app_settings.SESSION_REMEMBER is not None:
            del self.fields["remember"]
        try:
            reset_url = reverse("account_reset_password")
        except NoReverseMatch:
            pass
        else:
            forgot_txt = _("Forgot your password?")
            self.fields["password"].help_text = mark_safe(
                f'<a href="{reset_url}">{forgot_txt}</a>'
            )  # nosec
