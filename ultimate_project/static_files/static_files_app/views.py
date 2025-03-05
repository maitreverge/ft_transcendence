from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.middleware import csrf
from django.template import Context, Template
import requests
import os

def index(request):
    username = request.session.get("username")
    if "HX-Request" not in request.headers:
        return redirect("/home/")
    return render(request, "index.html", {"username": username, "request": request})

def login_form(request):
    csrf_token = csrf.get_token(request)
    return render(request, "login.html")

def login(request):
    username = request.POST.get("username")
    request.session["username"] = username
    return redirect("/")

def home(request):
    if request.headers.get("HX-Request"):
        return render(request, "partials/home.html")
    username = request.session.get("username")
    return render(request, "index.html", {"username": username, "page": "partials/home.html"})

def profile(request):
    if request.headers.get("HX-Request"):
        return render(request, "partials/profile.html")
    username = request.session.get("username")
    return render(request, "index.html", {"username": username, "page": "partials/profile.html"})

def stats(request):
    if request.headers.get("HX-Request"):
        return render(request, "partials/stats.html")
    username = request.session.get("username")
    return render(request, "index.html", {"username": username, "page": "partials/stats.html"})

def match_simple_template(request):
    page_html = requests.get("http://tournament:8001/tournament/simple-match/").text
    username = request.session.get("username")
    return render(
        request,
        "index.html",
        {
            "username": username,
            "rasp": os.getenv("rasp", "false"),
            "pidom": os.getenv("pi_domain", "localhost:8000"),
            # "simpleUsers": consumer.players,
            "page": page_html
        }
    )

def user_profile_template(request):
    page_html = requests.get("http://user:8004/user/profile/").text
    username = request.session.get("username")
    return render(
        request,
        "index.html",
        {
            "username": username,
            "rasp": os.getenv("rasp", "false"),
            "pidom": os.getenv("pi_domain", "localhost:8000"),
            # "simpleUsers": consumer.players,
            "page": page_html
        }
    )

def user_stats_template(request):
    page_html = requests.get("http://user:8004/user/stats/").text
    username = request.session.get("username")
    return render(
        request,
        "index.html",
        {
            "username": username,
            "rasp": os.getenv("rasp", "false"),
            "pidom": os.getenv("pi_domain", "localhost:8000"),
            # "simpleUsers": consumer.players,
            "page": page_html
        }
    )
