from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from user_management_app.models import Player
from django.shortcuts import redirect
from .forms import LoginForm, SigninForm

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "auth_app/index.html")

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            print(dict(request.POST.items()), flush=True)
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("auth_index"))
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    
    return render(request, "auth_app/login.html", {
        "title": "LOGIN PAGE",
        "form": form,
    })

def signin_view(request):
    if request.method == "POST":
        form = SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # Create user
            if not Player.objects.filter(username=username).exists():
                user = Player.objects.create_user(username=username, email=email, password=password)
                login(request, user)  # Auto-login after registration
                return redirect("auth_index")
            else:
                form.add_error("username", "Username already taken")
    else:
        form = SigninForm()

    return render(request, "auth_app/signin.html", {"title": "SIGNIN PAGE", "form": form})

def logout_view(request):
    """Logs out the user and redirects to login."""
    logout(request)
    return redirect("login")
