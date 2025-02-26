from django.contrib.auth.forms import AuthenticationForm, BaseUserCreationForm

class LoginForm(AuthenticationForm):
    pass

class SigninForm(BaseUserCreationForm):
    pass