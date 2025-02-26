from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "auth_app/login.html")

def login_view(request):
    if request.method == "POST":
        pass
        # print(list(request.POST.items()), flush=True)
    return render(request, "auth_app/login.html", {
        "title": "LOGIN PAGE"
    })

def signin_view(request):
    if request.method == "POST":
        pass
    return render(request, "auth_app/signin.html", {
        "title": "SIGNIN PAGE"
    })

def logout_view(request):
    pass
