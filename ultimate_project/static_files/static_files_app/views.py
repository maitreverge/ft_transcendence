from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.middleware import csrf
from django.template import Context, Template

def index(request):
    username = request.session.get("username")
    return render(request, "index.html", {"username": username})

def login_form(request):
    csrf_token = csrf.get_token(request)
    return render(request, "login.html")

def login(request):
    username = request.POST.get("username")
    request.session["username"] = username
    return redirect("/")

def home(request):
    return render(request, "partials/home.html")

def profil(request):
    if request.headers.get("HX-Request"):
        return render(request, "partials/profil.html")
    return render(request, "index.html", {"page": "partials/profil.html"})

def stats(request):
    return render(request, "partials/stats.html")
