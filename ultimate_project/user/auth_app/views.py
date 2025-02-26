from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import LoginForm, SigninForm

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "auth_app/login.html")

def login_view(request):
    if request.method == "POST":
        # pass
        print(dict(request.POST.items()), flush=True)
        # print(list(request.POST.items()), flush=True)
    return render(request, "auth_app/login.html", {
        "title": "LOGIN PAGE",
        "form": LoginForm(),
    })

def signin_view(request):
    if request.method == "POST":
        pass
    return render(request, "auth_app/signin.html", {
        "title": "SIGNIN PAGE",
        "form": SigninForm(),
    })

def logout_view(request):
    pass
