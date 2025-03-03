from django import forms
from django.contrib.auth.forms import AuthenticationForm
from user_management_app.models import Player


# Basic login form using Django's built-in authentication.
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"placeholder": "Username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )


# User registration form for new players.
class SigninForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"})
    )
    two_fa_enabled = forms.BooleanField(
        required=False, initial=False, label="Enable Two-Factor Authentication"
    )

    class Meta:
        model = Player
        fields = ["username", "email", "two_fa_enabled"]

    # Validate that passwords match.
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Passwords do not match")

        return cleaned_data

class TwoFaForm(forms.Form):
    token = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={"placeholder": "Enter 6-digit 2FA Token"})
    )

