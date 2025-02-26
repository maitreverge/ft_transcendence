from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    pass

class SigninForm(BaseUserCreationForm):
    pass