from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    # Define a username field with a maximum length of 254 characters
    username = forms.CharField(max_length=254)
    
    # Define a password field with a label "Password", no stripping of whitespace,
    # and a password input widget
    password = forms.CharField()

    # class Meta:
    #     # Specify the model to use for this form
    #     model = User
    #     # Define the fields to include in the form
    #     fields = ['username', 'password']