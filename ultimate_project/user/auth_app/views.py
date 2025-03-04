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
        print(dict(request.POST.items()), flush=True)
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            print(dict(request.POST.items()), flush=True)
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:

                # Check if user has 2FA enabled
                # if user.two_fa_enabled and not user.two_fa_verified:
                if user.two_fa_enabled:
                    print("2FA called on login", flush=True)
                    # Store user ID in session without logging them in
                    request.session['user_id_for_2fa'] = user.id
                    return redirect(reverse("check_2fa"))
                
                # If 2FA is not enabled, proceed with regular login
                login(request, user)
                return HttpResponseRedirect(reverse("auth_index"))
            else:
                print("Invalid username or password", flush=True)
                form.add_error("username", "Invalid username or password")
        else:
            print("Invalid form", flush=True)
            print(form.errors, flush=True)
    else:
        form = LoginForm()

    return render(
        request,
        "auth_app/login.html",
        {
            "title": "LOGIN PAGE",
            "form": form,
        },
    )


def signin_view(request):
    if request.method == "POST":
        form = SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            two_fa_enabled = form.cleaned_data["two_fa_enabled"]

            # Create user
            if not Player.objects.filter(username=username).exists():
                user = Player.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    two_fa_enabled=two_fa_enabled,
                )
                
                # If 2FA is enabled, we need to set up 2FA first
                if two_fa_enabled:
                    # Log the user in first so they can access setup_2fa
                    login(request, user)
                    request.session['user_id_for_2fa'] = user.id
                    return redirect("setup_2fa")
                else:
                    # If no 2FA, just log them in and redirect
                    login(request, user)
                    return redirect("auth_index")
            else:
                form.add_error("username", "Username already taken")
    else:
        form = SigninForm()

    return render(
        request, "auth_app/signin.html", {"title": "SIGNIN PAGE", "form": form}
    )


def logout_view(request):
    """Logs out the user and redirects to login."""
    logout(request)
    return redirect("login")
